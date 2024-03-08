import os
from PyPDF2 import PdfReader

class PDFLoader:
    def __init__(self, dirpath):
        self.dirpath = dirpath

    def load_pdfs(self):
        all_papers = []
        for root, dirs, files in os.walk(self.dirpath):
            for filename in files:
                if filename.endswith('.pdf'):
                    pdf_path = os.path.join(root, filename)
                    try:
                        reader = PdfReader(pdf_path)
                        text = [page.extract_text() for page in reader.pages if page.extract_text()]
                        all_papers.append(' '.join(text))
                    except Exception as e:
                        print(f"Error loading {filename}: {e}")
        return all_papers, True if all_papers else False
