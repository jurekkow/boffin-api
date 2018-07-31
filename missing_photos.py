import os

from PIL import Image

IN_IMAGES_DIR_PATH = os.path.join("data", "missing-images")
OUT_IMAGES_DIR_PATH = os.path.join("data", "images")
IMAGE_SIZE = (250, 250)


for image_file in os.listdir(IN_IMAGES_DIR_PATH):
    image_path = os.path.join(IN_IMAGES_DIR_PATH, image_file)
    image = Image.open(image_path)
    image.thumbnail(IMAGE_SIZE)
    out_image_path = os.path.join(OUT_IMAGES_DIR_PATH, f"{image_file[:-3]}png")
    image.save(out_image_path)
