from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/soccer', methods=['GET'])
def get_soccer_data():
    url = "https://oauth.reddit.com/r/soccer/new"
    access_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzEzMjE3NDA1LjY1MjE2NywiaWF0IjoxNzEzMTMxMDA1LjY1MjE2NywianRpIjoiZGh0bUl2OWhtbWtfS3BuUDBPY21zdTlvUzVlR3d3IiwiY2lkIjoiT0NnSUVNZzlqakxzakMtOW9zN1pCQSIsImxpZCI6InQyXzE1Y2s5MCIsImFpZCI6InQyXzE1Y2s5MCIsImxjYSI6MTQ4Njk1NzQxMTgyMiwic2NwIjoiZUp5S1Z0SlNpZ1VFQUFEX193TnpBU2MiLCJmbG8iOjl9.qWemxxA7kyw8XApWnHvOXYEre78iuQQbXe-ooyjUJ7Hd527HfamFMol-kuxF6nqpYl9UKS7XEuWZRWTv7PRPAesXInpqLm1G2Ic99MMUkIuwrWeWWLys4qH8eScQpQG7Cm1ZdrFojJlRXM0-p79lHdntIK9-jZguCmEanXfrdSFnIz1ud8OIZVbGmp6hvx6OxMCwshB-ccW_Um4glKQREfG9abJbxpwqHPb01nVZB6mjhsq1EAxGdXYno6MUTPLAZ3xM2jG2D3MlqoXsGe1SV9_3guzlIJZv2I-qUIcZXOzKJFqkFMHMJdKrwkxA4o043opoa9zh0-mxQTWH06MxLA'
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
        return jsonify({"error": "Failed to retrieve data from Reddit"}), response.status_code

if __name__ == '__main__':
    endpoint = 'http://127.0.0.1:8080/soccer'
    print(f"Flask API running at endpoint: \033[34m{endpoint}\033[0m\n")
    app.run(debug=True, port=8080)