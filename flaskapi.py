from flask import Flask, jsonify, render_template
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

token_info = {
    "access_token": None,
    "expires_at": 0
}

def generate_new_token():
    url = 'https://www.reddit.com/api/v1/access_token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f"Basic {os.getenv('REDDIT_AUTH')}",
    }
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        access = response.json()
        token_info["access_token"] = access["access_token"]
        token_info["expires_at"] = time.time() + access["expires_in"]
    else:
        print(f"Failed to generate token: {response.status_code} - {response.text}")

def get_token():
    if time.time() > token_info["expires_at"]:
        generate_new_token()
    return token_info["access_token"]

@app.route('/', methods=['GET'])
def get_soccer_data():
    url = "https://oauth.reddit.com/r/soccer/new"
    access_token = get_token()
    user_agent = "YourUserAgent/0.1 by YourRedditUsername"

    headers = {
        "Authorization": f"bearer {access_token}",
        "User-Agent": user_agent
    }
    
    params = {
        "limit": 50
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()["data"]["children"]
        formatted_data = [{"title": child["data"]["title"], "permalink": child["data"]["permalink"]} for child in data]
        return render_template('index.html', data=formatted_data)
    else:
        error_message = f"Failed to retrieve data: {response.status_code} - {response.text}"
        print(error_message)
        return jsonify({"error": error_message}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
