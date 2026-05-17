import fitz
import pytesseract

from pathlib import Path
from PIL import Image
from docx import Document


class TextExtractor:

    @staticmethod
    def extract_text(file_path: str) -> str:
        extension = Path(file_path).suffix.lower()

        extraction_methods = {
            ".pdf": TextExtractor.extract_pdf,
            ".docx": TextExtractor.extract_docx,
            ".txt": TextExtractor.extract_txt,
            ".png": TextExtractor.extract_image,
            ".jpg": TextExtractor.extract_image,
            ".jpeg": TextExtractor.extract_image,
        }

        extractor = extraction_methods.get(extension)

        if not extractor:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return extractor(file_path)

    @staticmethod
    def extract_pdf(file_path: str) -> str:
        text = []

        pdf = fitz.open(file_path)

        try:
            for page in pdf:
                page_text = page.get_text()

                if page_text.strip():
                    text.append(page_text)

        finally:
            pdf.close()

        return "\n".join(text).strip()

    @staticmethod
    def extract_docx(file_path: str) -> str:
        document = Document(file_path)

        text = [
            para.text.strip()
            for para in document.paragraphs
            if para.text.strip()
        ]

        return "\n".join(text)

    @staticmethod
    def extract_txt(file_path: str) -> str:
        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:
            return file.read().strip()

    @staticmethod
    def extract_image(file_path: str) -> str:
        image = Image.open(file_path)

        return pytesseract.image_to_string(image).strip()