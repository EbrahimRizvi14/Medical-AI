from formatter import PDFFormatter


class Chunker:
    def __init__(self, max_chars=1200):
        self.max_chars = max_chars
        self.blocks = PDFFormatter().merge_elements()

    def semantic_chunk(self):
        chunks = []
        current_chunk = ""
        current_heading = ""

        for block in self.blocks:
            t = block["type"]
            content = block["content"].strip()

            if t == "heading":
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                current_heading = content
                current_chunk = content + "\n"

            elif t in ("text", "table"):
                if len(current_chunk) + len(content) > self.max_chars:
                    chunks.append(current_chunk.strip())
                    current_chunk = current_heading + "\n"
                current_chunk += content + "\n"

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

chunker = Chunker()
chunks = chunker.semantic_chunk()
print(chunks)