import os

from config import KNOWLEDGE_FOLDER

from config import SUPPORTED_KNOWLEDGE_EXTENSIONS


def load_knowledge_documents():
    """
    Load text documents from the knowledge folder.
    """

    documents = []
    ids = []

    if not os.path.exists(KNOWLEDGE_FOLDER):
        return documents, ids

    for filename in os.listdir(KNOWLEDGE_FOLDER):

        
        if not any(
            filename.endswith(extension)
            for extension in SUPPORTED_KNOWLEDGE_EXTENSIONS
        ):
            continue
        


        filepath = os.path.join(KNOWLEDGE_FOLDER, filename)

        if not os.path.isfile(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as file:
            documents.append(file.read())
            ids.append(filename)

    return documents, ids