from img2table.document import PDF


def extract_tables(pdf_file):
    doc = PDF(pdf_file)
    result = doc.extract_tables(ocr=None)
    page_list = []
    for page in result.values():
        table_list = []
        for table in page:
            table_bbox = (
                table.bbox.x1,
                table.bbox.y1,
                table.bbox.x2,
                table.bbox.y2
            )
            table_html = (
                table.html
                .replace(' colspan="1"', '')
                .replace(' rowspan="1"', '')
                .replace('<table', '<table border="1"')
            )
            table_list.append((table_html, table_bbox))
        page_list.append(table_list)
    return page_list
