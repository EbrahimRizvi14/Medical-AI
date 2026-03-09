import fitz

doc = fitz.open("data/test1.pdf")

for page in doc:

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

    for p in paras:
        print(p)