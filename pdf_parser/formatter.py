from text_extractor import TextExtractor
from table_extractor import TableExtractor
from image_extractor import ImageExtractor


class PDFFormatter:
    def __init__(self):

        text_extractor = TextExtractor("data/test1.pdf")
        table_extractor = TableExtractor("data/test1.pdf")
        self.text = text_extractor.extract_text()
        self.tables = table_extractor.extract_tables()

        if text_extractor.is_scanned_pdf():
            self.ocr_texts = ImageExtractor("data/test1.pdf").extract_images()
        else:    
            self.ocr_texts = []

    def normalize_text(self):
        elements = []

        for page_num, page in enumerate(self.text, start=1):

            for block in page:

                text = block["content"]

                if block["type"] == "heading":
                    elements.append({
                        "type": "heading",
                        "page": page_num,
                        "content": text
                    })
                    continue

                paragraphs = text.split(". ")

                for p in paragraphs:
                    if len(p.strip()) < 40:
                        continue

                    elements.append({
                        "type": "text",
                        "page": page_num,
                        "content": p.strip()
                    })

        return elements

    def table_to_markdown(self, table):

        header = [str(cell) for cell in table[0]]
        rows = table[1:]

        md = "| " + " | ".join(header) + " |\n"

        md += "| " + " | ".join(["---"] * len(header)) + " |\n"

        for row in rows:
            clean_row = [str(cell) for cell in row]

            md += "| " + " | ".join(clean_row) + " |\n"
        
        return md

    def normalize_tables(self):
        elements = []

        for table_data in self.tables:
            page = table_data[0] or 1
            page = int(page)
            table = table_data[1]

            elements.append({
                "type": "table",
                "page": page,
                "content": self.table_to_markdown(table)
            })

        return elements

    def normalize_images(self):

        elements = []

        if self.ocr_texts is None:
            return elements
        
        for text in self.ocr_texts:

            cleaned = " ".join(text.split())

            if len(cleaned) < 20:
                continue

            for img in self.ocr_texts:
                elements.append({
                    "type": "image",
                    "page": img["page"],
                    "content": cleaned
                })

        return elements

    def merge_elements(self):

        elements = self.normalize_text() + self.normalize_tables() + self.normalize_images()

        elements.sort(key=lambda x: (x["page"], x.get("y", 0), x.get("x", 0)))

        return elements


if __name__ == "__main__":
    formatter = PDFFormatter()
    merged = formatter.merge_elements()

    print(merged)