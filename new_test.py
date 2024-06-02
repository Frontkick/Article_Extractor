import requests

def call_post_with_x_www_form_urlencoded(url, code):
    # Define the data to be sent in x-www-form-urlencoded format
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

# Example usage:
url = "https://cold-zaria-suckyou-eb2c31ea.koyeb.app/ortus"
code = "exit(5)"
response_text = call_post_with_x_www_form_urlencoded(url, code)
if response_text:
    print("Response:", response_text)
