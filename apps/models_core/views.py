from django.shortcuts import render
from django.http import JsonResponse
from .services import predict_image
from .train import download_dataset_from_s3,create_dataset_from_directory,train_famous_places_model
from apps.storage.services import download_from_s3
import tempfile
import os
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import threading
from .pipeline_services.pipeline_famous import famous_places_pipeline
from dataclasses import asdict
from django.http import JsonResponse

def predict_location(request):
    return JsonResponse({"lat": 25.197, "lon": 55.274})

def train_model(request):
    return JsonResponse({"message": "Training started"})

@csrf_exempt
def predict_place(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    
    print(request.FILES)
    print(request.POST)

    model_name = request.POST.get("model_name", "resnet_50_famous_places")
    image_file = request.FILES.get("file")
    s3_key = request.POST.get("s3_key")

    if not image_file and not s3_key:
        return JsonResponse({"error": "Provide file upload or s3_key"}, status=400)

    temp_path = None
    try:
        if image_file:
            temp_fd, temp_path = tempfile.mkstemp(suffix=os.path.splitext(image_file.name)[1])
            with os.fdopen(temp_fd, "wb") as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
        elif s3_key:
            temp_path = download_from_s3(s3_key)

        place_name,confidence = predict_image(model_name, temp_path)
        # pred_class_name, confidence = predict_image(model_name, temp_path)
        return JsonResponse({"place_name": place_name, "model": model_name})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

@csrf_exempt
def train_famous_places(request):

    if request.method != "POST":
        return JsonResponse({"error":"POST required"},status =405)
    
    epochs = int(request.POST.get("epochs",1))
    print(epochs)
    ## return JsonResponse({"epoch":epochs})
    def run_training():
        BUCKET_NAME = "mlopsp3"
        PREFIX = "50_most_famous_places"

        LOCAL_DIR = settings.BASE_DIR / "datasets/50_famous_places"
        SAVE_MODEL_PATH = settings.BASE_DIR / "models/resnet_50_famous_places.h5"
        print(BUCKET_NAME,PREFIX,LOCAL_DIR)
        download_dataset_from_s3(BUCKET_NAME,PREFIX,LOCAL_DIR)

        train_ds,val_ds = create_dataset_from_directory(str(LOCAL_DIR))

        # num_classes = len(train_ds.class_names)
        model, history = train_famous_places_model(train_ds=train_ds, val_ds=val_ds, epochs=epochs, save_path=str(SAVE_MODEL_PATH))

        print("Training complete!")

    # Run training in background thread (non-blocking)
    threading.Thread(target=run_training).start()
    return JsonResponse({"status": "Training started in background", "epochs": epochs})

@csrf_exempt
def famous_place_pipeline(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    
    print(request.FILES)
    print(request.POST)

    model_name = request.POST.get("model_name", "resnet_50_famous_places")
    image_file = request.FILES.get("file")
    s3_key = request.POST.get("s3_key")
    org_iata = request.POST.get("org_iata")
    depart_date = request.POST.get("depart_date")
    return_date = request.POST.get("return_date")

    if not image_file and not s3_key:
        return JsonResponse({"error": "Provide file upload or s3_key"}, status=400)

    temp_path = None
    try:
        if image_file:
            temp_fd, temp_path = tempfile.mkstemp(suffix=os.path.splitext(image_file.name)[1])
            with os.fdopen(temp_fd, "wb") as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
        elif s3_key:
            temp_path = download_from_s3(s3_key)

        result = famous_places_pipeline(model_name,temp_path,org_iata,depart_date,return_date)
        # return JsonResponse(asdict(result), safe=False)
        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
