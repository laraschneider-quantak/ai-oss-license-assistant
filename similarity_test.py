from openai import OpenAI
from math import sqrt

client = OpenAI(
    api_key="api_keyxyz"
)


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def cosine_similarity(a, b):

    dot_product = sum(x * y for x, y in zip(a, b))

    magnitude_a = sqrt(sum(x * x for x in a))
    magnitude_b = sqrt(sum(y * y for y in b))

    return dot_product / (magnitude_a * magnitude_b)


mit_embedding = get_embedding("MIT License")
bsd_embedding = get_embedding("BSD License")
gpl_embedding = get_embedding("GPL v3")
football_embedding = get_embedding("Football Match")


print("MIT vs BSD")
print(cosine_similarity(mit_embedding, bsd_embedding))

print("\nMIT vs GPL")
print(cosine_similarity(mit_embedding, gpl_embedding))

print("\nMIT vs Football")
print(cosine_similarity(mit_embedding, football_embedding))