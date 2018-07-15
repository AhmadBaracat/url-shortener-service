from flask import Flask

app = Flask(__name__)


@app.route("/")
def root():
    return ''


@app.route('/<shortened_url>', methods=['GET'])
def get_shortened_url(shortened_url):
    return ''


@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    return ''
