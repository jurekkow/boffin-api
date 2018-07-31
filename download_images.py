import asyncio
import io
import itertools
import json
import os

import aiohttp
from PIL import Image

import paths

DEFAULT_FILENAME = ""
IMAGES_DIR_PATH = os.path.join("data", "images")
DEFAULT_IMAGE_SIZE = (250, 250)
CHUNK_SIZE = 50


async def get_image_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


def save_image(image_data, image_path, out_size=DEFAULT_IMAGE_SIZE):
    image = Image.open(io.BytesIO(image_data))
    image.thumbnail(out_size)
    image.save(image_path)


async def create_image(artist, url):
    print(f"Downloading image for {artist} from {url}...")
    try:
        image_data = await get_image_data(url)
    except aiohttp.InvalidURL:
        print(f"Couldn't download image for {artist} from {url}")
        return DEFAULT_FILENAME, artist
    image_file_name = f"{artist.lower().replace(' ', '-').replace('/', '')}.png"
    image_path = os.path.join(IMAGES_DIR_PATH, image_file_name)
    print(f"Saving image for {artist} in {image_path}")
    try:
        save_image(image_data, image_path)
    except OSError:
        print(f"Couldn't download image for {artist} from {url}")
        return DEFAULT_FILENAME, artist
    return image_file_name, artist


def chunks(container, chunk_size=CHUNK_SIZE):
    for i in range(0, len(container), chunk_size):
        yield container[i:i + chunk_size]


async def get_artists_images(fests):
    artists = list(itertools.chain.from_iterable(fests.values()))
    artists_images = {}
    for artists_chunk in chunks(artists):
        image_futures = [
            create_image(artist["name"], artist["imageUrl"])
            for artist in artists_chunk
        ]
        done_image_futures, _ = await asyncio.wait(image_futures)
        for image_future in done_image_futures:
            image_file_name, artist = image_future.result()
            artists_images[artist] = image_file_name
    return artists_images


def create_fests_img(fests, artists_images):
    fests_img = {}
    for year, artists in fests.items():
        fests_img[year] = [
            {
                "name": artist["name"],
                "imageFileName": artists_images.get(artist["name"], DEFAULT_FILENAME),
                "tags": artist["tags"]
            }
            for artist in artists
        ]
    return fests_img


async def main():
    with open(paths.FESTS_FILE_PATH) as fests_file:
        fests = json.load(fests_file)

    artists_images = await get_artists_images(fests)
    fests_img = create_fests_img(fests, artists_images)

    with open(paths.FESTS_IMG_FILE_PATH, "w") as fests_img_file:
        json.dump(fests_img, fests_img_file)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
