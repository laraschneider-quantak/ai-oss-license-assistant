from openai import OpenAI

client = OpenAI(
    api_key="sk-proj-test"
)

response = client.responses.create(
    model="gpt-5",
    input="What is the MIT License?"
)

print(response.output_text)