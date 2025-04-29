import numpy as np
from .patch_img2table import PATCH_PAGE_DPI
from .extract_tables import extract_tables
from .extract_paragraphs import extract_paragraphs
from .reading_order import recursive_xy_cut


def intersects(bbox1, bbox2):
    ax1, ay1, ax2, ay2 = bbox1
    bx1, by1, bx2, by2 = bbox2
    return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)


def get_sorted_text(sections):
    boxes = [np.round(section[1]) for section in sections]
    boxes_array = np.asarray(boxes).astype(int)
    if boxes_array.ndim == 1:
        boxes_array = boxes_array.reshape(-1, 4)
    res = []
    recursive_xy_cut(boxes_array, np.arange(len(boxes)), res)
    sorted_text = []
    for i in res:
        sorted_text.append(sections[i][0].strip("\n").strip())
    return sorted_text


def get_page_text(sections, tables):
    # filter sections that are not part of the tables
    all_sections = []
    for section in sections:
        is_in_table = False
        for table in tables:
            if intersects(section[1], table[1]):
                is_in_table = True
                break
        if not is_in_table:
            all_sections.append(section)
    # add tables
    for table in tables:
        all_sections.append(table)
    # sort by reading order
    if len(all_sections) > 0:
        sorted_texts = get_sorted_text(all_sections)
    else:
        sorted_texts = []
    # result
    return "\n\n".join(sorted_texts)


def extract_content(pdf_file):
    section_result = extract_paragraphs(pdf_file, PATCH_PAGE_DPI)
    table_result = extract_tables(pdf_file)
    all_pages = []
    for i in range(len(section_result)):
        page_text = get_page_text(section_result[i], table_result[i])
        all_pages.append(page_text)
    return all_pages
