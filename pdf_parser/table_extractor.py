import fitz

doc = fitz.open("data/test1.pdf")
page_number = 0

for page in doc:
    page_number += 1
    tables = page.find_tables().tables
    for table in tables:
        print(f'Table found in page {page_number}')
        print(table.bbox)
        
        table_data = table.extract()
        clean_rows = []

        for row in table_data:
            filled = sum(cell is not None and cell.strip() != "" for cell in row)

            if filled > 1:
                clean_rows.append(row)

        for row in clean_rows:
            print(row)