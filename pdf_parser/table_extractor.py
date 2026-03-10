import fitz
class TableExtractor:
    def __init__(self, pdf_path):
        self.doc = fitz.open(pdf_path)

    def extract_tables(self):
        page_number = 0

        for page in self.doc:

            page_number += 1
            self.tables = page.find_tables().tables

            for table in self.tables:
                print(f'Table found in page {page_number}')
                print(table.bbox)
                
                table_data = table.extract()
                clean_rows = []

                if len(table_data) < 2:
                    continue

                for row in table_data:
                    filled = sum(cell is not None and cell.strip() != "" for cell in row)

                    if filled > 1:
                        clean_rows.append(row)


if __name__ == "__main__":
    extractor = TableExtractor("data/sample2.pdf")
    extractor.extract_tables()