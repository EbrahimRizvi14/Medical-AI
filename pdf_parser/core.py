from text_extractor import TextExtractor
from table_extractor import TableExtractor
from image_extractor import ImageExtractor

text_extractor = TextExtractor("data/test1.pdf")
table_extractor = TableExtractor("data/test1.pdf")
text = text_extractor.extract_text()
tables = table_extractor.extract_tables()

if text_extractor.is_scanned_pdf():
    ocr_texts = ImageExtractor("data/test1.pdf").extract_images()
else:    
    ocr_texts = []

def normalize_text(text_output):
    elements = []

    for page_num, page in enumerate(text_output, start=1):

        paragraphs = " ".join(page).split(". ")

        for p in paragraphs:
            if len(p.strip()) < 40:
                continue

            elements.append({
                "type": "text",
                "page": page_num,
                "content": p.strip()
            })

    return elements

def table_to_markdown(table):

    header = [str(cell) for cell in table[0]]
    rows = table[1:]

    md = "| " + " | ".join(header) + " |\n"

    md += "| " + " | ".join(["---"] * len(header)) + " |\n"

    for row in rows:
        clean_row = [str(cell) for cell in row]

        md += "| " + " | ".join(clean_row) + " |\n"
    
    return md

def normalize_tables(tables):
    elements = []

    for table_data in tables:
        page = table_data[0] or 1
        page = int(page)
        table = table_data[1]

        elements.append({
            "type": "table",
            "page": page,
            "content": table_to_markdown(table)
        })

    return elements

def normalize_images(ocr_outputs):

    elements = []

    if ocr_outputs is None:
        return elements
    
    for text in ocr_outputs:

        cleaned = " ".join(text.split())

        if len(cleaned) < 20:
            continue

        for img in ocr_outputs:
            elements.append({
                "type": "image",
                "page": img["page"],
                "content": cleaned
            })

    return elements

def merge_elements(text_elems, table_elems, image_elems):

    elements = text_elems + table_elems + image_elems

    elements.sort(key=lambda x: (x["page"], x.get("y", 0), x.get("x", 0)))

    return elements

print(merge_elements(
    normalize_text(text),
    normalize_tables(tables),
    normalize_images(ocr_texts)
))
