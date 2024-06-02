
from flask import Flask,request, jsonify
from flask_cors import CORS
import requests

from dotenv import load_dotenv
import os

def call_post_with_x_www_form_urlencoded(code):
    # Define the data to be sent in x-www-form-urlencoded format
    url = "https://cold-zaria-suckyou-eb2c31ea.koyeb.app/ortus"
    data = {
        'code': code
    }

    try:
        # Make the POST request with requests.post()
        response = requests.post(url, data=data)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("POST request successful!")
            # Return the response text
            return response.text
        else:
            print("POST request failed with status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

app = Flask(__name__)
CORS(app)

load_dotenv()

@app.route('/api', methods=['POST'])
def process_post_request():
    # Get the 'code' parameter from the POST request
    code = request.form.get('code')

    # Check if 'code' parameter is present
    if code:
        # Process the code (you can replace this with any logic you want)
        output = call_post_with_x_www_form_urlencoded(code)
        # Return the output as JSON
        return jsonify({"output": output})
    else:
        # If 'code' parameter is missing, return an error message
        return jsonify({"error": "No 'code' parameter provided"}), 400


@app.route('/')
def start():
    return "Server is running"


if __name__ == '__main__':
    app.run(debug=True, port=4000)
