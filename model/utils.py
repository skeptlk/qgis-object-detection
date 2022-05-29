from rasterio import Affine, MemoryFile
from rasterio.enums import Resampling
from contextlib import contextmanager
import numpy as np
import re


def get_im_index(s, offset=4):
    m = re.search(r'\d+$', s[:-offset])
    return m.group() if m else None


@contextmanager
def np_to_geotiff(tiff_np, profile):
    """Convert np array of shape (x, x, 3) to rasterio tiff file"""
    tiff_np = tiff_np.swapaxes(1, 2)
    tiff_np = tiff_np.swapaxes(0, 1)
    with MemoryFile() as memfile:
        with memfile.open(**profile) as dataset:
            dataset.write(tiff_np)
            del tiff_np

        with memfile.open() as dataset:
            yield dataset


@contextmanager
def rescale_image(src, width: int):
    t = src.transform

    # rescale the metadata
    scale = width / src.width
    height = int(src.height * scale)
    transform = Affine(t.a / scale, t.b, t.c, t.d, t.e / scale, t.f)

    profile = src.profile
    profile.update(transform=transform, driver='GTiff',
                   height=height, width=width)

    data = src.read(
        # Note changed order of indexes, arrays are band, row, col order not row, col, band
        out_shape=(src.count, height, width),
        resampling=Resampling.bilinear,
    )

    with MemoryFile() as memfile:
        with memfile.open(**profile) as dataset:  # Open as DatasetWriter
            dataset.write(data)
            del data

        with memfile.open() as dataset:  # Reopen as DatasetReader
            yield dataset  # Note yield not return


def stretch_min_max(x, lower, upper):
    """Min-max contrast stretch"""
    x[x < lower] = lower
    x[x > upper] = upper
    x_norm = ((x - lower) / (upper - lower)) * 255
    return x_norm


def normalize(x, lower, upper):
    """Normalize an array to a given bound interval"""
    x_max = np.max(x)
    x_min = np.min(x)
    m = (upper - lower) / (x_max - x_min)
    x_norm = (m * (x - x_min)) + lower
    return x_norm


def normalize_colors(img):
    img_norm = []
    for i in range(img.shape[0]):
        std = img[i].std()
        mean = img[i].mean()
        min = mean - 2 * std
        max = mean + 2 * std
        band = stretch_min_max(img[i], min, max)
        img_norm.append(band)
    img_norm = np.array(img_norm)
    img_norm = img_norm.astype("uint8")
    img_norm = img_norm.swapaxes(0, 1)
    img_norm = img_norm.swapaxes(1, 2)
    return img_norm
