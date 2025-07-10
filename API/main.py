import requests

ticker="aapl"
token="2b98850831e2141f5e107ce99d26dcb6c48a98d0"

url=f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?token={token}"

response=requests.get(url)
print(response.status_code)
print(response.json())

