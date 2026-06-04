import os
from math import sqrt
from openai import OpenAI


# Verbindung zur OpenAI API herstellen
client = OpenAI(
    api_key="DEIN_API_KEY"
)


# Ordner mit unserem Wissen
folder = "knowledge"


# Text -> Embedding (Vektor) umwandeln
def get_embedding(text):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


# Ähnlichkeit zwischen zwei Embeddings berechnen
def cosine_similarity(a, b):

    # Skalarprodukt berechnen
    dot_product = sum(x * y for x, y in zip(a, b))

    # Länge von Vektor A
    magnitude_a = sqrt(sum(x * x for x in a))

    # Länge von Vektor B
    magnitude_b = sqrt(sum(y * y for y in b))

    # Cosine Similarity zurückgeben
    return dot_product / (magnitude_a * magnitude_b)


# Hier speichern wir alle Dokumente
documents = []


# Alle Dateien im knowledge-Ordner durchlaufen
for filename in os.listdir(folder):

    # Vollständigen Dateipfad erzeugen
    filepath = os.path.join(folder, filename)

    # Datei öffnen und Inhalt lesen
    with open(filepath, "r", encoding="utf-8") as file:

        content = file.read()

    # Dokument + Embedding speichern
    documents.append({
        "filename": filename,
        "content": content,
        "embedding": get_embedding(content)
    })


# Frage des Benutzers
query = "Which license requires source code disclosure?"


# Embedding für die Frage erzeugen
query_embedding = get_embedding(query)


# Beste Übereinstimmung vorbereiten
best_score = -1
best_document = None


# Alle Dokumente vergleichen
for document in documents:

    # Ähnlichkeit zwischen Frage und Dokument berechnen
    score = cosine_similarity(
        query_embedding,
        document["embedding"]
    )

    print(f'{score:.4f} - {document["filename"]}')

    # Falls dieses Dokument besser passt:
    if score > best_score:

        best_score = score
        best_document = document


# Bestes Dokument anzeigen
print("\nBest document:")
print(best_document["filename"])
print(best_document["content"])


# GPT bekommt:
# - die Frage
# - das gefundene Dokument
response = client.responses.create(
    model="gpt-5",
    input=f"""
Answer the question using only the information below.

Information:
{best_document["content"]}

Question:
{query}
"""
)


# Antwort von GPT ausgeben
print("\nLLM Answer:")
print(response.output_text)