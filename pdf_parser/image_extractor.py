import pytesseract
from PIL import Image
import io
import fitz

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Ebrahim\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

class ImageExtractor:
    def __init__(self, pdf_path):
        self.doc = fitz.open(pdf_path)

    def extract_images(self, ocr=False):
        seen = set()

        for page_number, page in enumerate(self.doc):
            
            self.page = page_number + 1
            image_list = page.get_images(full=True)

            for image_index, img in enumerate(image_list):

                if ocr:

                    xref = img[0]

                    if xref in seen:
                        continue

                    seen.add(xref)

                    width, height = img[2], img[3]

                    if width < 100 or height < 100:
                        continue

                    base_image = self.doc.extract_image(xref)
                    image_bytes = base_image["image"]

                    image = Image.open(io.BytesIO(image_bytes))

                    text = pytesseract.image_to_string(image)

                    if len(text.strip()) < 5:
                        continue 
                        
                    return text

if __name__ == "__main__":
    extractor = ImageExtractor("data/test1.pdf")
    print(extractor.extract_images(ocr=True))