from openai import OpenAI

client = OpenAI(
    api_key= "sk-projxyz"
)

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="MIT License"
)

embedding = response.data[0].embedding

print(type(embedding))
print(len(embedding))
print(embedding[:10])
