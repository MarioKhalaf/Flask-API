import requests

url = 'https://www.reddit.com/api/v1/access_token'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic T0NnSUVNZzlqakxzakMtOW9zN1pCQToyYXpjcE9UTFB2dkNudzNDY0ZCYi1MaTBsUGM2YUE=',
}
data = {
    'grant_type': 'password',
    'username': 'abomario',
    'password': 'makh1572'
}

response = requests.post(url, headers=headers, data=data)
access = response.json()
print(access)