import fitz  # PyMuPDF
import docx
import io

class DocumentParser:
    @staticmethod
    def extract_text(uploaded_file) -> str:
        """Extracts text from PDF, DOCX, or TXT securely."""
        if uploaded_file is None:
            return ""
            
        filename = uploaded_file.name.lower()
        text = ""

        try:
            if filename.endswith('.pdf'):
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                for page in doc:
                    text += page.get_text("text") + "\n"
            elif filename.endswith('.docx'):
                doc = docx.Document(io.BytesIO(uploaded_file.read()))
                text = "\n".join([para.text for para in doc.paragraphs])
            elif filename.endswith('.txt'):
                text = uploaded_file.read().decode('utf-8')
        except Exception as e:
            raise ValueError(f"Error parsing document: {str(e)}")
            
        return text.strip()