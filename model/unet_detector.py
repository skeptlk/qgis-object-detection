from PIL import Image
from model.utils import crop_image, normalize_colors
from model.models import unet
import rasterio
import numpy as np
import random
import os

class UnetDetector():
  def __init__(self) -> None:
    self.model = unet()
    self.model.load_weights(os.environ['UNET_WEIGHTS_FILE'])
    
  def mask_to_wkt(self, mask) -> str:
    return mask
    return "POLYGON ((533193.1015783922 174038.23070064266, 533193.0385603837 174038.41525338194, 533194.6229692716 174038.95627105064, 533194.6983712668 174038.7354509218, 533194.879708215 174038.79737085517, 533195.0604846688 174038.26795409713, 533193.0052700456 174037.56617349468, 533192.8121096052 174038.1318576422, 533193.1015783922 174038.23070064266))"

  def prediction_to_mask(self, prediction):
    msk = prediction.squeeze()
    msk = np.stack((msk,)*3, axis=-1)
    msk[msk >= 0.5] = 1 
    msk[msk < 0.5] = 0 
    return msk.astype("uint8")

  def prepare_image(self, raw):
    # normalize colors
    np_norm = normalize_colors(raw.read([1,2,3]))
    # for now we don't rescale, just fit image in 512x512 square
    return crop_image(np_norm)

  def detect(self, filename):
    tif = rasterio.open(filename)
    img = self.prepare_image(tif)
    pred = self.model.predict(np.expand_dims(img, 0))
    mask = self.prediction_to_mask(pred)
    mask[mask == 1] = 255
    im = Image.fromarray(mask)
    im.save("uploads/" + str(random.randrange(1000, 9999)) + ".png")
    return self.mask_to_wkt(mask)
