from pdfminer.high_level import extract_pages, LAParams
from pdfminer.layout import LTTextBoxHorizontal


def pts_to_px(bbox_pts, page_height, dpi=200):
    factor = dpi / 72
    x0, y0, x1, y1 = bbox_pts
    minx, maxx = min(x0, x1), max(x0, x1)
    miny, maxy = min(y0, y1), max(y0, y1)
    return (minx * factor,
            (page_height - maxy) * factor,
            maxx * factor,
            (page_height - miny) * factor)


def intersects(bbox1, bbox2):
    ax1, ay1, ax2, ay2 = bbox1
    bx1, by1, bx2, by2 = bbox2
    return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)


def extract_paragraphs(pdf_file, dpi=200):
    pages = extract_pages(pdf_file, laparams=LAParams(), caching=False)
    page_list = []
    for page in pages:
        page_height = page.height
        text_lines = []
        for element in page:
            if isinstance(element, (LTTextBoxHorizontal)):
                text_lines.append((element.get_text(),
                                   pts_to_px(element.bbox, page_height, dpi)))
        page_list.append(text_lines)
    return page_list
