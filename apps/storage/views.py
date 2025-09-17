from django.shortcuts import render

import os
from django.http import JsonResponse
from django.conf import settings
from .services import download_from_s3,upload_to_s3,download_images_with_csv

def upload_image(request):
    """
    POST endpoint to upload an image to S3.
    Use form-data with key='file'.

    curl -X POST http://127.0.0.1:8000/api/v1/storage/upload/ \
    -F "file=@/path/to/your/image.jpg"

    """
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file provided"}, status=400)

    # Save temporarily in local folder
    temp_path = f"/tmp/{uploaded_file.name}"
    with open(temp_path, "wb+") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    try:
        s3_key = upload_to_s3(temp_path, s3_folder="test_images")
        return JsonResponse({"message": "File uploaded", "s3_key": s3_key})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def download_dataset(request):

    """
    Example: GET /api/v1/storage/download/?folder=fam_places
    """

    folder = request.GET.get("folder")
    if not folder:
        return JsonResponse({"error": "folder parameter is required"}, status=400)

    try:
        local_dir = download_from_s3(settings.AWS_STORAGE_BUCKET_NAME, folder)
        return JsonResponse({"message": "Dataset downloaded", "local_dir": local_dir})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    
    # output_dir = "datasets/yfcc26k_sample/images"
    # csv_path = "datasets/yfcc26k_sample/labels.csv"
    # download_images_with_csv(output_dir, csv_path, n_samples=10)
    # return JsonResponse({"msg":"success"})
        
