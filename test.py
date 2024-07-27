import requests as axios

response = axios.get("https://669f704cb132e2c136fdd9a0.mockapi.io/api/v1/retreats")
retreatList = response.json()

# for retreat in retreatList[0]:
print((retreatList[0]))