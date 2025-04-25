from .patch_img2table import PATCH_PAGE_DPI
from .extract_tables import extract_tables
from .extract_paragraphs import extract_paragraphs


def intersects(bbox1, bbox2):
    ax1, ay1, ax2, ay2 = bbox1
    bx1, by1, bx2, by2 = bbox2
    return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)


def get_page_text(sections, tables):
    output = []
    table_set = set()
    for section in sections:
        section_text, section_bbox = section
        is_in_table = False
        for i in range(len(tables)):
            table_text, table_bbox = tables[i]
            if intersects(section_bbox, table_bbox):
                if i not in table_set:
                    table_set.add(i)
                    output.append(table_text)
                is_in_table = True
                break
        if not is_in_table:
            output.append(section_text.strip("\n").strip())
    return "\n\n".join(output)


def extract_content(pdf_file):
    section_result = extract_paragraphs(pdf_file, PATCH_PAGE_DPI)
    table_result = extract_tables(pdf_file)
    all_pages = []
    for i in range(len(section_result)):
        page_text = get_page_text(section_result[i], table_result[i])
        all_pages.append(page_text)
    return all_pages
