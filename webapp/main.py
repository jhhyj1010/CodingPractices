from fastapi import FastAPI, UploadFile, HTTPException, File
from PIL import Image
from datetime import datetime
import os, shutil


app = FastAPI()  # Create an App

UPLOAD_LOCATION = "uploaded_images"
os.makedirs(UPLOAD_LOCATION, exist_ok=True)
MAX_FILE_SIZE = 5 * 1024 * 1024  # Max image size
IMAGES_HISTORY = {}  # For saving images history information
PWD = os.getcwd()  # Get current directory


@app.post("/upload_compressed_images/")
async def upload_compressed_images(file: UploadFile = File(...), quality=50):
    # Check whether the image being uploaded is legal
    if not file.headers["content-type"].startswith("image/"):
        raise HTTPException(status_code=400, detail="Only images are allowed")

    # Check image size
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 5MB")

    # Check disk usage upfront in case of failures during storing images
    disk_free = shutil.disk_usage(PWD).free
    if disk_free < file.size:
        raise HTTPException(
            status_code=400, detail="No space left for storing current image"
        )

    # Upload uploaded image to the specified folder
    original_filename = "original-" + file.filename
    original_full_path = f"{PWD}/{UPLOAD_LOCATION}/{original_filename}"
    with open(original_full_path, "wb") as f:
        f.write(await file.read())
    uploaded_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Compress the original image
    compressed_filename = "compressed-" + file.filename
    compressed_full_path = f"{PWD}/{UPLOAD_LOCATION}/{compressed_filename}"
    with Image.open(original_full_path) as img:
        img.save(compressed_full_path, quality=quality, optimize=True)
    compressed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store the image information in a dictionary
    IMAGES_HISTORY[file.filename] = {
        "Original Image": original_full_path,
        "Uploaded Time": uploaded_time,
        "Compressed Image": compressed_full_path,
        "Compressed Quality": quality,
        "Compressed Time": compressed_time,
        "Initial Size(MB)": file.size / 1024 / 1024,
    }
    return IMAGES_HISTORY


@app.get("/get_images_history/")
async def get_images_history():
    return [{"file name": k, "file information": v} for k, v in IMAGES_HISTORY.items()]


@app.post("/remove_image/<image_name>")
async def remove_image(image_name):
    original_filename = "original-" + image_name
    original_full_path = f"{PWD}/{UPLOAD_LOCATION}/{original_filename}"
    compressed_filename = "compressed-" + image_name
    compressed_full_path = f"{PWD}/{UPLOAD_LOCATION}/{compressed_filename}"
    os.system(f"rm -f {original_full_path}")
    os.system(f"rm -f {compressed_full_path}")
