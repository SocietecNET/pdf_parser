import img2table.document.pdf as pdf_mod
import pypdfium2
import cv2
from img2table.document.base.rotation import fix_rotation_image
import img2table.ocr.pdf as ocr_mod
from pypdfium2 import PdfTextPage

PATCH_PAGE_DPI = 108


def images_144(self):
    if self._images is not None:
        return self._images
    doc = pypdfium2.PdfDocument(input=self.bytes)
    imgs = []
    for i in (self.pages or range(len(doc))):
        page = doc[i]
        img = cv2.cvtColor(page.render(scale=PATCH_PAGE_DPI/72).to_numpy(),
                           cv2.COLOR_BGR2RGB)
        if self.detect_rotation:
            final, self._rotated = fix_rotation_image(img=img)
        else:
            final, self._rotated = img, False
        imgs.append(final)
    self._images = imgs
    doc.close()
    return imgs


def get_char_coordinates_144(
    text_page: PdfTextPage, idx_char: int,
    page_width: float, page_height: float,
    page_rotation: int, x_offset: float, y_offset: float
):
    _x1, _y1, _x2, _y2 = text_page.get_charbox(idx_char, loose=True)
    if _x1 == _x2 and _y1 == _y2:
        _x1, _y1, _x2, _y2 = text_page.get_charbox(idx_char, loose=False)
    # rotation handling (same as original)…
    # then scale at 144 DPI:
    x1 = int((_x1 - x_offset) * PATCH_PAGE_DPI/72)
    y1 = int((page_height - _y2 + y_offset) * PATCH_PAGE_DPI/72)
    x2 = int((_x2 - x_offset) * PATCH_PAGE_DPI/72)
    y2 = int((page_height - _y1 + y_offset) * PATCH_PAGE_DPI/72)
    return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)


pdf_mod.PDF.images = property(images_144)
ocr_mod.get_char_coordinates = get_char_coordinates_144
