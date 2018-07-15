import random
import string
import validators
from flask import Flask
from flask import jsonify
from flask import request

SHORTENED_URL_LENGTH = 10
SHORTENED_URL_ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits

app = Flask(__name__)


@app.route("/")
def root():
    return ''


@app.route('/<shortened_url>', methods=['GET'])
def get_shortened_url(shortened_url):
    return ''


@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    is_valid, error_response = is_valid_post_request(request)

    if not is_valid:
        return error_response

    url = extract_url_from_request()
    key = ''.join(random.choices(SHORTENED_URL_ALPHABET, k=SHORTENED_URL_LENGTH))

    return jsonify({"shortened_url": key}), 201


def is_valid_post_request(request):
    # Make sure that the request header was set correctly and
    # that the request contains json body
    if not request.is_json or request.get_json(False, True, True) is None:
        return False, generate_error_msg("Your request should contain valid json body")

    url = extract_url_from_request()

    if url == '':
        return False, generate_error_msg("Please provide a url to be shortened")

    if not validators.url(url):
        return False, generate_error_msg("Please provide a valid url")

    return True, None


def extract_url_from_request():
    return request.get_json().get('url', '')


def generate_error_msg(msg):
    return jsonify({"error_message": msg}), 400
