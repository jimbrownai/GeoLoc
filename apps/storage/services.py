# apps/storage/services.py
import os, requests, csv, random
import boto3 
from django.conf import settings
from urllib.parse import urlencode
import pandas as pd
import random


def upload_to_s3(file_path: str, s3_folder: str = "test_images") -> str:

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

    filename = os.path.basename(file_path)
    s3_key = f"{s3_folder}/{filename}"

    s3.upload_file(file_path, settings.AWS_STORAGE_BUCKET_NAME, s3_key)

    return s3_key

def download_from_s3(bucket_name:str,s3_folder: str, local_dir: str = None):

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

    if not local_dir:
        local_dir = os.path.join(settings.LOCAL_DATA_DIR, s3_folder.strip("/"))
    os.makedirs(local_dir, exist_ok=True)

    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name, Prefix=s3_folder):
        if "Contents" not in page:
            continue
        for obj in page["Contents"]:
            key = obj["Key"]
            if key.endswith("/"):  # skip folder placeholders
                continue

            # preserve folder structure
            local_path = os.path.join(local_dir, os.path.relpath(key, s3_folder))
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            if not os.path.exists(local_path):  
                s3.download_file(bucket_name, key, local_path)
                print(f"Downloaded {key} → {local_path}")
                # s3.download_file(bucket_name, key, local_path)

    return local_dir

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

def list_s3_objects(bucket_name, prefix=""):
    """
    List all objects under a prefix in S3
    """
    s3 = get_s3_client()
    objects = []

    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get("Contents", []):
            objects.append(obj["Key"])

    return objects
    
WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php?"

def fetch_geotagged_images(lat, lon, radius=1000, limit=20):
    """
    Fetch geotagged image URLs near a given lat/lon from Wikimedia Commons
    """
    params = {
        "action": "query",
        "generator": "geosearch",
        "ggsprimary":"all",
        "ggsnamespace":6,
        "ggscoord": f"{lat}|{lon}",
        "ggsradius": radius,
        "ggslimit": limit,
        "prop": "coordinates|imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth":200,
        "iiurlheight":200,
        "format": "json"
    }
    HEADERS = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) ")}
    url = WIKIMEDIA_API + urlencode(params)
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()

    images = []
    if "query" in data:
        for _, page in data["query"]["pages"].items():
            if "imageinfo" in page:
                if "coordinates" in page:
                        img_url = page["imageinfo"][0]["url"]
                        lat = page["coordinates"][0]["lat"]
                        lon = page["coordinates"][0]["lon"]
                        images.append({"title": page["title"], "lat": lat, "lon": lon, "url": img_url})
    print(f"Downloaded - {len(images)}")
    return images

def get_random_city_coords(cities_csv="worldcities.csv", max_pop=200000):
    """
    Pick a random city above a population threshold, return lat/lon
    """
    df = pd.read_csv( os.path.join("datasets",cities_csv))

    # "city","city_ascii","lat","lng","country","iso2","iso3","admin_name","capital","population","id"
    # filter to larger/populated cities for better chance of images
    df = df[df["population"] >= max_pop]

    row = df.sample(1).iloc[0]

    # add small random offset (~10 km) to avoid always hitting city center
    lat = row["lat"] + random.uniform(-0.1, 0.1)
    lon = row["lng"] + random.uniform(-0.1, 0.1)

    return lat, lon, row["city"], row["country"]

def download_images_with_csv(output_dir, csv_path, n_samples=100, radius = 10000,limit=150):

    os.makedirs(output_dir, exist_ok=True)
    HEADERS = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) ")}
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["image_path","lat","lon","city", "country"])

        for i in range(n_samples):
            lat, lon, city, country = get_random_city_coords() 
            print(f"Fetching images near {city}, {country} ({lat:.4f}, {lon:.4f})")

            urls = fetch_geotagged_images(lat,lon,radius=radius, limit=limit)
            for j,url in enumerate(urls):

                try: 
                    img_data = requests.get(url=url['url'],headers=HEADERS, timeout=10).content
                    filename = f"{i}_{j}.jpg"
                    file_path = os.path.join(output_dir, filename)
                    with open(file_path,"wb") as img_file:
                        img_file.write(img_data)
                    writer.writerow([file_path,lat,lon,city, country])
                except Exception as e:
                    print(f"failed to download {url}: {e}")
