from flask import Flask, render_template, request
from inverted_index import *
data_path = './data/'

import json
app = Flask(__name__)


@app.route('/')
def Index():
    with open(data_path +'json_files/ucl/tweets_2021-11-24.json') as file:
        data = json.load(file)
    return render_template('index.html', consultas = data)

@app.route('/consulta', methods=['POST'])
def SearchQuery():
    if request.method == 'POST':
        query = request.form['query']
        k = request.form['tweets']
        valor_k = int(k)
        data = retrieve_tweets(query, valor_k)
        data = json.loads(data)
        return render_template('index.html', consultas = data)

if __name__ == '__main__':
    app.run(port = 3000, debug = True)