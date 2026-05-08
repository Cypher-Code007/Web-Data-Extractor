import os
from flask import Flask, render_template, request

# This tells Flask to look for templates in the same folder as this script
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    target_url = ""
    
    if request.method == 'POST':
        target_url = request.form.get('url')
        try:
            # Adding a User-Agent makes the request look like a real browser
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(target_url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Logic: Extracting all headlines and links
                headlines = [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3'])[:10]]
                links = [a['href'] for a in soup.find_all('a', href=True)[:10]]
                
                results = {"headlines": headlines, "links": links}
            else:
                results = {"error": f"Failed to reach site. Status Code: {response.status_code}"}
        except Exception as e:
            results = {"error": str(e)}

    return render_template('index.html', results=results, url=target_url)

if __name__ == '__main__':
    app.run(debug=True)

