from flask import Flask, render_template
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)