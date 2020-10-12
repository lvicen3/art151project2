from flask import Flask,render_template
app = Flask(__name__)

from bs4 import BeautifulSoup
import requests
import re

@app.route('/')
def hello_world():
    return render_template("index.html")

