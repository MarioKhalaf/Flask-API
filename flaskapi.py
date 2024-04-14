import datetime
from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

token_info = {
    "access_token": None,
    "expires_at": datetime.utcnow()
}

# Function to check the validity of the token
def is_token_valid():
    return datetime.utcnow() < token_info["expires_at"]

# Function to refresh the access token
def refresh_access_token():
    # Replace these with your Reddit app credentials
    client_id = 'YOUR_CLIENT_ID'
    client_secret = 'YOUR_CLIENT_SECRET'
    username = 'abomario'
    password = 'makh1572
    

    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }
    headers = {
        'User-Agent': 'YourUserAgent/0.1 by YourRedditUsername'
    }
    
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    res.raise_for_status()  # Check for request failure
    token = res.json()
    
    token_info["access_token"] = token['access_token']
    # Assuming the token expires in 1 hour by default
    token_info["expires_at"] = datetime.utcnow() + datetime.timedelta(seconds=token['expires_in'])

@app.route('/', methods=['GET'])
def get_soccer_data():
    url = "https://oauth.reddit.com/r/all"
    access_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzExNzEyODgwLjkzNjQ4NiwiaWF0IjoxNzExNjI2NDgwLjkzNjQ4NiwianRpIjoiZ2pRTkpCbURNQkVzSWlLbThmNEQzNzRKZVFPNmdBIiwiY2lkIjoiT0NnSUVNZzlqakxzakMtOW9zN1pCQSIsImxpZCI6InQyXzE1Y2s5MCIsImFpZCI6InQyXzE1Y2s5MCIsImxjYSI6MTQ4Njk1NzQxMTgyMiwic2NwIjoiZUp5S1Z0SlNpZ1VFQUFEX193TnpBU2MiLCJmbG8iOjl9.Thwb2oM0RL_oaUaUyxE0lpcEVnOOsHdSaVMEnrkSYB0xidzYhCjjS3LnJkCMdNSxle6HsGEzQqvDrAQVvKV0IqH1FrG-qzPYpknQlSMp1QobYxzbeAPwxUETd5PyDHDLIiSLab7gPpb4WgFkMli-covrXfQAf-YyAtVUDsamCPzFHY21XlKTcvB4H2Pt_Fy3eCx4plIgFksSX12bWMZ6Jmtti9u220s-bpd1gIW_UQLaKRbzWn2dxwLsYS1aduKVhg-fi2sGKWbbHOD8EpKo1EiXvNcWdi1IcEtoUZzGhdHWDjx3m7ylopliXVntOW029aOoellFZH-HIsJd1hyZuA'
    user_agent = "YourUserAgent/0.1 by YourRedditUsername"

    headers = {
        "Authorization": f"bearer {access_token}",
        "User-Agent": user_agent
    }
    
    params = {
        "limit": 500
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()["data"]["children"]
        formatted_data = [{"title": child["data"]["title"], "permalink": child["data"]["permalink"]} for child in data]
        return render_template('index.html', data=formatted_data)
    else:
        return jsonify({"error": "Failed to retrieve data from Reddit"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=8080)