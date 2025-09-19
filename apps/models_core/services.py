import os
import tensorflow as tf
import numpy as np 
from django.conf import settings
import tf_keras as keras 
import tensorflow_hub as hub 
from tensorflow.keras.preprocessing import image 

MODEL_REGISTRY = {
    'yfcc26k_geolocate':{
        # geolocation_backend\apps\models_core\models\yfcc26\yfccRegV1.keras
        "path": os.path.join(settings.BASE_DIR, "apps","models_core","models", "yfcc26/yfccRegV1.keras"),
        "classes":None,
        "model":None
    },
    'resnet_50_famous_places':{
        "path": os.path.join(settings.BASE_DIR, "apps","models_core","models", "famous_places_model"),
        "classes": ["Acropolis_of_Athens",
                    "Angkor_Wat",
                    "Arc_de_Triomphe",
                    "Atomium",
                    "Berlin_Museum_Island",
                    "Big_Ben",
                    "Blue_Mosque",
                    "Bodiam_Castle",
                    "Brandenburg_Gate",
                    "Burj_Khalifa",
                    "Casa_Mila",
                    "Chateau_Frontenac",
                    "Chichen_Itza_Mexico",
                    "Christ_the_Redeemer",
                    "Dancing_House",
                    "Dresden_Frauenkirche",
                    "Eiffel_Tower",
                    "Ephesus",
                    "Flatiron_Building",
                    "Gateway_Arch",
                    "Giants_Causeway",
                    "Golden_Gate_Bridge",
                    "Guggenheim_Museum",
                    "Hagia_Sophia",
                    "Helsinki_Cathedral",
                    "Kremlin",
                    "Le_Centre_Pompidou",
                    "Leaning_Tower_of_Pisa",
                    "Lincoln_Center",
                    "Machu_Picchu",
                    "Milan_Cathedral",
                    "Millau_Bridge",
                    "Mont_St_Michel",
                    "Musee_dOrsay",
                    "Musee_du_Louvre",
                    "Neuschwanstein_Castle",
                    "Osaka_Castle",
                    "Oxford_University",
                    "Sagrada_Familia",
                    "Space_Needle",
                    "Sultan_Ahmed_Mosque",
                    "Sydney_Harbor_Bridge",
                    "Sydney_Opera_House",
                    "The_Great_Sphinx",
                    "The_Pyramids_of_Giza",
                    "Tian_Tan_Buddha",
                    "Tower_Bridge",
                    "Washington_Monument",
                    "White_House",
                    "statue_of_liberty"],
        "model": None
    },
    'mobnet_50_famous_places':{
        "path": os.path.join(settings.BASE_DIR, "apps","models_core","models", "famous_places_model_mobnet"),
        "classes": ["Acropolis_of_Athens",
                    "Angkor_Wat",
                    "Arc_de_Triomphe",
                    "Atomium",
                    "Berlin_Museum_Island",
                    "Big_Ben",
                    "Blue_Mosque",
                    "Bodiam_Castle",
                    "Brandenburg_Gate",
                    "Burj_Khalifa",
                    "Casa_Mila",
                    "Chateau_Frontenac",
                    "Chichen_Itza_Mexico",
                    "Christ_the_Redeemer",
                    "Dancing_House",
                    "Dresden_Frauenkirche",
                    "Eiffel_Tower",
                    "Ephesus",
                    "Flatiron_Building",
                    "Gateway_Arch",
                    "Giants_Causeway",
                    "Golden_Gate_Bridge",
                    "Guggenheim_Museum",
                    "Hagia_Sophia",
                    "Helsinki_Cathedral",
                    "Kremlin",
                    "Le_Centre_Pompidou",
                    "Leaning_Tower_of_Pisa",
                    "Lincoln_Center",
                    "Machu_Picchu",
                    "Milan_Cathedral",
                    "Millau_Bridge",
                    "Mont_St_Michel",
                    "Musee_dOrsay",
                    "Musee_du_Louvre",
                    "Neuschwanstein_Castle",
                    "Osaka_Castle",
                    "Oxford_University",
                    "Sagrada_Familia",
                    "Space_Needle",
                    "Sultan_Ahmed_Mosque",
                    "Sydney_Harbor_Bridge",
                    "Sydney_Opera_House",
                    "The_Great_Sphinx",
                    "The_Pyramids_of_Giza",
                    "Tian_Tan_Buddha",
                    "Tower_Bridge",
                    "Washington_Monument",
                    "White_House",
                    "statue_of_liberty"],
        "model": None
    }
}

def load_model_by_name(model_name:str):
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model {model_name}")
    model_info = MODEL_REGISTRY[model_name]

    if model_info["model"] is None:
        if model_name == 'resnet_50_famous_places' or model_name == 'mobnet_50_famous_places':
            model_info["model"] = keras.models.load_model(
                model_info["path"],
                custom_objects= {'KerasLayer':hub.KerasLayer}
            )
        else:
            model_info["model"] = tf.keras.models.load_model(model_info["path"])
    return model_info

def load_and_preprocess(img_path):
    img =  image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 127.5 - 1.0   # normalize to [-1,1]
    img_array = np.expand_dims(img_array, axis=0)  # add batch dimension
    return img_array

def predict_image(model_name:str, image_path:str):
    model_info = load_model_by_name(model_name)
    model = model_info["model"]

    img = load_and_preprocess(image_path)

    preds = model.predict(img)                # shape: (1, 50)

    if model_info["classes"]:
        pred_class_idx = np.argmax(preds, axis=1)[0]
        confidence = preds[0][pred_class_idx]
        pred_class_name = model_info["classes"][pred_class_idx]
        # return {"place_name":pred_class_name, "confidence":confidence.astype(float)}
        return pred_class_name, confidence.astype(float)
    else:
        lat = float(preds[0][0]) * 90.0
        lon = float(preds[0][1]) * 180.0
        return {"lat": lat, "lon": lon}


def run_training():
    # TODO: implement training pipeline
    return "Training done"

def run_prediction(image_path: str):
    # TODO: implement model prediction
    return {"lat": 25.197, "lon": 55.274}
