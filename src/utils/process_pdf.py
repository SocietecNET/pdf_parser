import io
import pypdfium2
from .extract_content import extract_content


def process_pdf(pdf_bytes, page_from, page_to):
    # Create PDF from bytes
    pdf = pypdfium2.PdfDocument(pdf_bytes)

    # Select pages (0-indexed)
    start = page_from - 1 if page_from else 0
    end = page_to if page_to else len(pdf)
    pages = range(start, end)

    # Create new PDF with selected pages
    new_pdf = pypdfium2.PdfDocument.new()
    new_pdf.import_pages(pdf, pages)

    # Save to memory buffer
    buffer = io.BytesIO()
    new_pdf.save(buffer)
    buffer.seek(0)

    # Process the PDF
    return extract_content(buffer)
