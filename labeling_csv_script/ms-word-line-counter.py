from docx import Document

def count_lines_in_docx(file_path):
    """ Count only non-empty lines in a Word document. """
    doc = Document(file_path)
    line_count = sum(1 for p in doc.paragraphs if p.text.strip())
    return line_count

file_path = "./labeling_csv_script/recordings/Kurdi.Text-Cleaned.docx"
line_count = count_lines_in_docx(file_path)
print(f"Total number of non-empty lines: {line_count}")