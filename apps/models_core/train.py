# apps/models_core/train.py
import os
import tensorflow as tf
from apps.storage.services import list_s3_objects, download_from_s3
from .services import load_model_by_name
from django.conf import settings


def download_dataset_from_s3(bucket_name: str, prefix: str, local_dir: str):
    """
    Download entire S3 folder to local directory
    """
    os.makedirs(local_dir, exist_ok=True)
    keys = list_s3_objects(bucket_name, prefix)  # Returns all object keys under prefix
    download_from_s3(bucket_name,prefix,local_dir)
    # for key in keys:
    #     relative_path = key.replace(prefix + "/", "")
    #     local_path = os.path.join(local_dir, relative_path)
    #     os.makedirs(os.path.dirname(local_path), exist_ok=True)
    #     download_from_s3(key, local_path)

    print(f"Dataset downloaded to {local_dir}")

import tensorflow as tf

def create_dataset_from_directory(dataset_dir: str, img_size=(224, 224), batch_size=32, validation_split=0.2):
    """
    Create tf.data.Dataset for training and validation
    """
    train_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        labels='inferred',
        label_mode='int',
        validation_split=validation_split,
        subset="training",
        seed=42,
        image_size=img_size,
        batch_size=batch_size
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        labels='inferred',
        label_mode='int',
        validation_split=validation_split,
        subset="validation",
        seed=42,
        image_size=img_size,
        batch_size=batch_size
    )

    # Prefetch for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds

def train_famous_places_model(train_ds, val_ds, epochs=10, save_path=None):
    model = load_model_by_name('resnet_50_famous_places')['model']
    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)
    if save_path:
        model.save(save_path)
    return model, history