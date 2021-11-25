from flask import Flask, render_template, request
import json
app = Flask(__name__)

@app.route('/')
def Index():
    with open('tweets.json') as file:
        data = json.load(file)
    return render_template('index.html', consultas = data)

@app.route('/search_query', methods=['POST'])
def SearchQuery():
    if request.method == 'POST':
        query = request.form['query']
        print(query)
        return "recibido"

if __name__ == '__main__':
    app.run(port = 3000, debug = True)