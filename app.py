import aiohttp
from flask import Flask, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
from newspaper import Article
import google.generativeai as genai
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()

async def fetch_article_content(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        article_text = "\n".join([p.get_text() for p in soup.find_all('p')])
        return article_text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_summary(prompt):
  # Configure the API key
  api_key = os.getenv("GEMINI_KEY")
  genai.configure(api_key=api_key)

  # Create a GenerativeModel instance
  model = genai.GenerativeModel('gemini-pro')

  # Generate content using the prompt
  response = model.generate_content(prompt)

  # Return the generated text
  return response.text




async def search_articles(query, num_results=10):
    api_key = os.getenv("API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&num={num_results}"
    

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                items = data.get('items', [])

                articles = []  # Store articles in a list
                for item in items:
                    article_title = item.get('title')
                    article_url = item.get('link')
                    
                    article_content = await fetch_article_content(article_url)

                    if article_content:

                        summary = get_summary("Summarize this article in 5 points and it should be only 5 points"+article_content)
                        articles.append({'title': article_title, 'url': article_url,"summary":summary})  # Append each article to the list

                return articles  # Return the list of articles
            else:
                return None  # Return None if request failed


@app.route('/api/<string:param>', methods=['GET'])
async def get_request(param):
    articles = await search_articles(param)
    if articles:
        response = {
            'articles': articles
        }
    else:
        response = {
            'message': 'Failed to fetch search results.'
        }
    return jsonify(response)
@app.route('/')
def start():
    return "Server is running"


if __name__ == '__main__':
    app.run(debug=True, port=4000)
