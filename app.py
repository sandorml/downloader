from flask import Flask, render_template, make_response, request, send_from_directory
import threading
import urllib.request
import time
import signal
import os


app = Flask(__name__)

download_list = []
error_list = []


@app.route('/',  methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        name = request.form['name']
        download_list.append((url,name))
    
    downloads = os.listdir("./files")
    downloads.pop(0)
    return make_response(render_template('index.html', links = download_list, errors = error_list, downloads=downloads ))

@app.route('/dl/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory="./files", filename=filename)



def download():
    sleep = 0
    while True:
        if len(download_list):
            url, name = download_list.pop()
            filename = f"files/{name}"  
            try:
                urllib.request.urlretrieve(url=url, filename=filename)
            except:
                error_list.append(f"{name} could not be downloaded")           
        else:
            sleep = 120
        time.sleep(sleep)



thread = threading.Thread(target=download)
thread.start()
    
def signal_handler():
    thread.join(1)

signal.signal(signal.SIGINT , signal_handler)
app.run(host='0.0.0.0', port=8000, debug=False)

