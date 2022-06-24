from PIL import Image
from server.utils.wkt_helpers import get_wkt_multipolygons
from model.regularization.boundary_regularization import boundary_regularization
from model.utils import crop_image, normalize_colors
from model.models import unet
import rasterio
import numpy as np
import random
import cv2
import os


class UnetDetector():
  def __init__(self) -> None:
    self.model = unet((640, 640, 3))
    self.model.load_weights(os.environ['UNET_WEIGHTS_FILE'])

  def georeference_contours(self, contours: list, transform: rasterio.Affine) -> list:
    ref_contours = []
    for contour in contours:
      ref_c = []
      for (x, y) in contour:
        px, py = rasterio.transform.xy(transform, y, x, offset='center')
        ref_c.append([px, py])
      ref_contours.append(ref_c)

    return ref_contours
    
  def mask_to_wkt(self, mask, transform: rasterio.Affine) -> str:
    mask2 = cv2.medianBlur(mask, 5)
    mask2 = cv2.cvtColor(mask2, cv2.COLOR_BGR2GRAY)
    ret, mask2 = cv2.threshold(mask2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask2, connectivity=8)
    contours = []
    for i in range(1, num_labels):
      img = np.zeros_like(labels)
      index = np.where(labels==i)
      img[index] = 255
      img = np.array(img, dtype=np.uint8)

      regularization_contour = boundary_regularization(img).astype(np.int32)
      contours.append(regularization_contour)

    contours = self.georeference_contours(contours, transform)
    
    return get_wkt_multipolygons(contours)

  def prediction_to_mask(self, prediction):
    msk = prediction.squeeze()
    msk = np.stack((msk,)*3, axis=-1)
    thresh = 0.4
    msk[msk >= thresh] = 1 
    msk[msk < thresh] = 0 
    return msk.astype("uint8")

  def prepare_image(self, raw):
    # normalize colors
    np_norm = normalize_colors(raw.read([1,2,3]))
    # for now just fit image in square
    return crop_image(np_norm, out_shape = (640, 640))

  def detect(self, filename, app):
    self.app = app
    tif = rasterio.open(filename)
    img = self.prepare_image(tif)
    pred = self.model.predict(np.expand_dims(img, 0))
    mask = self.prediction_to_mask(pred)
    mask[mask == 1] = 255
    # save for debug
    im = Image.fromarray(mask)
    im.save("uploads/" + str(random.randrange(1000, 9999)) + ".png")
    return self.mask_to_wkt(mask, tif.transform)
