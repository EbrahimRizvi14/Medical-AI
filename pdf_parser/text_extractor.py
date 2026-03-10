import fitz
from table_extractor import TableExtractor

class TextExtractor:
    def __init__(self, pdf_path):
        self.doc = fitz.open(pdf_path)
        self.table_extractor = TableExtractor(pdf_path).extract_tables()

    def extract_text(self):
        for page in self.doc:

            page_dict = page.get_text("dict")
            blocks = page_dict["blocks"]

            text_blocks = [block for block in blocks if block["type"] == 0]
            text_blocks_sorted = sorted(text_blocks, key=lambda b: (b["bbox"][1], b["bbox"][0]))

            lines = []

            for block in text_blocks_sorted:
                for line in block["lines"]:
                    line_text = " ".join(span["text"] for span in line["spans"])
                    line_text = " ".join(line_text.split())           
                    line_text = line_text.replace("\uf0b7", "•")


                    if line_text.strip() in self.table_extractor.tables:
                        print(f"Table text found: {line_text.strip()}")
                        continue

                    if line_text:
                        y = line["bbox"][1]
                        lines.append((y, line_text))

            paras = []
            current_para = []
            prev_y = None
            threshold = 12

            for y, text in lines:
                if prev_y is None:
                    current_para.append(text)

                elif abs(y - prev_y) < threshold:
                    current_para.append(text)

                else:
                    paras.append(" ".join(current_para))
                    current_para = [text]

                prev_y = y

            if current_para:
                paras.append(" ".join(current_para))

if __name__ == "__main__":
    extractor = TextExtractor("data/sample2.pdf")
    print(extractor.extract_text())