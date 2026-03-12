import fitz

class TableExtractor:
    def __init__(self, pdf_path):
        self.doc = fitz.open(pdf_path)

    def extract_tables(self):

        all_tables = []

        for page_number, page in enumerate(self.doc, start=1):

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
                    
                if clean_rows:
                    all_tables.append((page_number, clean_rows))
                    
        return all_tables
            
    def return_tables(self):

        for page_number, page in enumerate(self.doc, start=1):
            tables = page.find_tables().tables
            
        return tables
                


if __name__ == "__main__":
    extractor = TableExtractor("data/test1.pdf")
    print(extractor.extract_tables())