from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/search_query', methods=['POST'])
def SearchQuery():
    if request.method == 'POST':
        query = request.form['query']
        print(query)
        return "recibido"

if __name__ == '__main__':
    app.run(port = 3000, debug = True)