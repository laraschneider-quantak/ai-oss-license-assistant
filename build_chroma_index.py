import os
import chromadb
from pypdf import PdfReader


# PDF-Datei lesen
def read_pdf(filepath):

    reader = PdfReader(filepath)

    full_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            full_text += text + "\n"

    return full_text


# Ordner mit Dokumenten
folder = "knowledge"


# ChromaDB öffnen
chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="oss_compliance_knowledge"
)

documents = []
ids = []


# Alle Dateien durchlaufen
for filename in os.listdir(folder):

    filepath = os.path.join(folder, filename)

    if filename.endswith(".txt"):

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

    elif filename.endswith(".pdf"):

        content = read_pdf(filepath)

    else:
        continue

    documents.append(content)
    ids.append(filename)

    print(f"Loaded: {filename}")


collection.upsert(
    documents=documents,
    ids=ids
)

print("Chroma index built successfully.")
print(f"Indexed documents: {len(documents)}")