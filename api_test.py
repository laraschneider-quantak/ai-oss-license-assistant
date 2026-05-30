import requests

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

print(response.status_code)

data = response.json()

print(type(data))
print(data[0])
print(data[0].keys())

for user in data:
    print(f'{user["name"]} - {user["email"]}')
    print(f'{user["name"]} - {user["address"]["city"]}')