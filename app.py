from flask import Flask, render_template, make_response, request
from flask.json import jsonify
import threading
import urllib.request
import time
import signal

app = Flask(__name__)

download_list = []

@app.route('/',  methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        name = request.form['name']
        download_list.append((url,name))
    return make_response(render_template('index.html'))




def download():
    sleep = 0
    while True:
        if len(download_list):
            url, name = download_list.pop()
            filename = f"files/{name}"            
            with urllib.request.urlopen(url) as file:
                with open(filename, 'wb') as f:
                    f.write(file.read())
        else:
            # sleep = 1200
            sleep = 2
        time.sleep(sleep)


hilo1 = threading.Thread(target=download)
hilo1.start()
    
def signal_handler():
    hilo1.join(1)

signal.signal(signal.SIGINT , signal_handler)
app.run(host='0.0.0.0', port=8000, debug=True)

