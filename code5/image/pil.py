# Needed on case-insensitive filesystems
from __future__ import absolute_import

# Try to import PIL in either of the two ways it can be installed.
try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    import Image
    import ImageDraw

import code5.image.base


class PilImage(code5.image.base.BaseImage):
    """
    PIL image builder, default format is PNG.
    """
    kind = "PNG"

    def new_image(self, **kwargs):
        img = Image.new("RGB", (self.pixel_size, self.pixel_size), "white")
        self._idr = ImageDraw.Draw(img)
        return img

    def drawrect(self, colour, row, col):
        box = self.pixel_box(row, col)
        self._idr.rectangle(box, fill=colour)

    def readrect(self, row, col):
        color = 0
        box = self.pixel_box(row, col)
        if self.loaded[box[0][0], box[0][1]] == 255 and self.loaded[box[1][0], box[1][1]] == 255:
            color = 255
        return color


    def save(self, stream, kind=None):
        if kind is None:
            kind = self.kind
        self._img.save(stream, kind)

    def load(self, image_path):
         self._img = Image.open(image_path)
         self._idr = ImageDraw.Draw(self._img)
         self.loaded = self._img.load()

    def __getattr__(self, name):
        return getattr(self._img, name)
