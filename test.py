import google.generativeai as genai
import os
def get_summary(prompt):
  # Configure the API key
  api_key = "AIzaSyBgNowjsrUl999xjzIheZ2mwa4oj7LhLm4"
  genai.configure(api_key=api_key)

  # Create a GenerativeModel instance
  model = genai.GenerativeModel('gemini-pro')

  # Generate content using the prompt
  response = model.generate_content(prompt)

  # Return the generated text
  return response.text


res = get_summary("you are  summarizer who summarize the article into 5 and only 5 points and also add '\n' after each point atricle: "+"batman")
file = open('test.txt','w')
file.write(res)
file.close()