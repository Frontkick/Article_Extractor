import aiohttp
from flask import Flask, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
from newspaper import Article
import time

app = Flask(__name__)
CORS(app)


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


async def get_summary(prompt):
    api_key = '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'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": "you are a summarizer which summarize all the text into 5 points and also extract 5 keywords from the summary "},
                            {"role": "user", "content": prompt}
                        ]

                    }
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data['choices'][0]['message']['content']
    except Exception as e:
        return str(e)


async def search_articles(api_key, search_engine_id, query, num_results=10):
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
                        time.sleep(2)
                        summary = await get_summary(article_content)
                        sum_error = "429 Client Error: Too Many Requests for url: https://api.openai.com/v1/chat/completions"
                        sum_error2 = "429, message='Too Many Requests', url=URL('https://api.openai.com/v1/chat/completions')"
                        sum_error3 = "400, message='Bad Request', url=URL('https://api.openai.com/v1/chat/completions')"
                        if summary != sum_error2 :
                            if summary!=sum_error3:
                                articles.append({'title': article_title, 'url': article_url,"summary":summary})  # Append each article to the list

                return articles  # Return the list of articles
            else:
                return None  # Return None if request failed


@app.route('/api/<string:param>', methods=['GET'])
async def get_request(param):
    articles = await search_articles(api_key, search_engine_id, param)
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
    api_key = "AIzaSyDgs-7ixnQARDlL2iVKk5SNTu5KhduwOiE"
    search_engine_id = "d5e0315085b194afb"
    app.run(debug=True, port=4000)
