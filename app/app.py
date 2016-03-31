import logging
import os

from flask import Flask, render_template, request, redirect, url_for, send_file

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s')

logger = logging.getLogger(__name__)

logger.debug("Starting flask...")

app = Flask(__name__, static_url_path='')

@app.route('/')
def splash():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
