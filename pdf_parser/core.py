from text_extractor import TextExtractor
from table_extractor import TableExtractor
from image_extractor import ImageExtractor


text = TextExtractor("data/test1.pdf").extract_text()
tables = TableExtractor("data/test1.pdf").extract_tables()
ocr_texts = ImageExtractor("data/test1.pdf").extract_images(ocr=True)

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

    header = [str(x) for x in table[0]]
    rows = table[1:]

    md = "| " + " | ".join(header) + " |\n"
    md += "| " + " | ".join(["---"] * len(header)) + " |\n"

    for row in rows:
        clean_row = [str(cell) for cell in row]
        md += "| " + " | ".join(clean_row) + " |\n"

    return md

def repair_table(table):
    fixed = []

    for row in table:
        new_row = []

        for cell in row:
            if isinstance(cell, list):
                cell = "".join(cell)

            cell = str(cell)

            if "|" in cell:
                cell = cell.replace("|", " ")

            new_row.append(cell.strip())

        fixed.append(new_row)

    return fixed

def normalize_tables(tables):
    elements = []

    for table_data in tables:
        page = table_data[0] or 1
        page = int(page)
        table = table_data[1]

        table = repair_table(table)

        elements.append({
            "type": "table",
            "page": page,
            "content": table_to_markdown(table)
        })

    return elements

def normalize_images(ocr_outputs):

    elements = []

    for text in ocr_outputs:

        cleaned = " ".join(text.split())

        if len(cleaned) < 20:
            continue

        elements.append({
            "type": "image",
            "page": ocr_outputs.page_number,
            "content": cleaned
        })

    return elements

def merge_elements(text_elems, table_elems, image_elems):

    elements = text_elems + table_elems + image_elems

    elements.sort(key=lambda x: int(x["page"]))

    return elements

print(merge_elements(
    normalize_text(text),
    normalize_tables(tables),
    normalize_images(ocr_texts)
))