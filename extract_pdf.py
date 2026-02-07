import PyPDF2

pdf_file = open(r'c:\Users\mdani\Downloads\Zweden-Trip-2026.docx.pdf', 'rb')
reader = PyPDF2.PdfReader(pdf_file)

text = ''
for page in reader.pages:
    text += page.extract_text() + '\n'

print(text)
pdf_file.close()
