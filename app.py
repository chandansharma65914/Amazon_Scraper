from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)

@app.route('/api/products', methods=['POST', 'HEAD'])
def get_product_details():
    if request.method == 'POST':
        data = request.get_json()
        asins = data.get('asins', [])
        result = {}

        for asin in asins:
            result[asin] = crawl_by_id(asin)

        return jsonify(result)
    elif request.method == 'HEAD':
        # Handle HEAD request (optional)
        return '', 200

def crawl_by_id(id):
    o = {}
    target_url = f"https://www.amazon.com/dp/{id}"
    headers = {
        "accept-language": "en-US,en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }
    
    resp = requests.get(target_url, headers=headers)

    if resp.status_code != 200:
        return {'error': f'Failed to fetch data for ASIN: {id}'}

    soup = BeautifulSoup(resp.text, 'html.parser')

    try:
        o["title"] = soup.find('h1', {'id': 'title'}).text.lstrip().rstrip()
    except:
        o["title"] = None

    images = re.findall('"hiRes":"(.+?)"', resp.text)
    o["thumbnail"] = images[0] if images else None

    try:
        o["price"] = soup.find("span", {"class": "a-price"}).find("span").text
    except:
        o["price"] = None

    try:
        o["productDescription"] = soup.find("div", {"id": "productDescription"}).text
    except:
        o["productDescription"] = None

    return o
