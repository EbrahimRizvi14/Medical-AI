import fitz
from table_extractor import TableExtractor

class TextExtractor:
    def __init__(self, pdf_path):
        self.doc = fitz.open(pdf_path)
        self.table_extractor = TableExtractor(pdf_path).return_tables()
        self.body_font_size = self.get_body_font_size()

    def get_body_font_size(self):

        sizes = []

        for page in self.doc:
            page_dict = page.get_text("dict")
            blocks = page_dict["blocks"]

            text_blocks = [block for block in blocks if block["type"] == 0]

            for block in text_blocks:
                for line in block["lines"]:
                    for span in line["spans"]:
                        sizes.append(span["size"])
        
        if not sizes:
            return 12

        return max(set(sizes), key=sizes.count)

    def extract_text(self):

        paragraphs = []

        for page in self.doc:

            page_dict = page.get_text("dict")
            blocks = page_dict["blocks"]

            text_blocks = [block for block in blocks if block["type"] == 0]
            text_blocks_sorted = sorted(text_blocks, key=lambda b: (b["bbox"][1], b["bbox"][0]))

            lines = []

            for block in text_blocks_sorted:
                for line in block["lines"]:
                    line_text = " ".join(span["text"] for span in line["spans"])
                    font_sizes = [span["size"] for span in line["spans"]]
                    max_size = max(font_sizes)
                    line_text = " ".join(line_text.split())           
                    line_text = line_text.replace("\uf0b7", "•")

                    is_heading = False

                    if max_size > self.body_font_size:
                        if len(line_text.split()) <= 12:
                            is_heading = True

                    if line_text.strip() in self.table_extractor:
                        print(f"Table text found: {line_text.strip()}")
                        continue

                    if line_text:
                        y = line["bbox"][1]
                        lines.append((y, line_text, is_heading))

            paras = []
            current_para = []
            prev_y = None
            threshold = 12

            for y, text, is_heading in lines:
                
                if is_heading:
                    
                    if text.strip() in ["•", "-", "*", "_"]:
                        continue
                    
                    if paras and paras[-1]["type"] == "heading":
                        paras[-1]["content"] += " " + text.strip()
                    else:
                        paras.append({"type": "heading", "content": text.strip()})

                    prev_y = None
                    current_para = []
                    continue

                if prev_y is None:
                    current_para.append(text)

                elif abs(y - prev_y) < threshold:
                    current_para.append(text)

                else:

                    paras.append({
                    "type": "paragraph",
                    "content": " ".join(current_para)
                })
                    current_para = [text]

                prev_y = y

            if current_para:
                paras.append({
                    "type": "paragraph",
                    "content": " ".join(current_para)
                })

            paragraphs.append(paras)

        return paragraphs
    
    def is_scanned_pdf(self):

        total_chars = 0

        for page in self.doc:
            total_chars += len(page.get_text())

        return total_chars < 500

if __name__ == "__main__":
    extractor = TextExtractor("data/test1.pdf")
    for i in extractor.extract_text():
            print(i)

    print(extractor.is_scanned_pdf())