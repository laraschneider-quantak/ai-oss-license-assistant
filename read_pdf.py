from pypdf import PdfReader

reader = PdfReader("test.pdf")

print(f"Pages: {len(reader.pages)}")

page = reader.pages[0]

text = page.extract_text()

print(text)