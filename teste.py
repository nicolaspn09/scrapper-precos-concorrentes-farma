import requests

url = "https://big-product-data.p.rapidapi.com/gtin/7896009498244"

headers = {
	"x-rapidapi-key": "2047e8ac72msh65c5d0fa878ad57p1c9d73jsn3be954aa0f6a",
	"x-rapidapi-host": "big-product-data.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())
