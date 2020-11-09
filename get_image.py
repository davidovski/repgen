import requests

q = "pig"

url = "http://www.splashbase.co/api/v1/images/search?query=" + q

r = requests.get(url = url)
data = r.json()

print(data["images"][0]["url"])