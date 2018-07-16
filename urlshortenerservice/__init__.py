import random
import string

import redis
import validators
from flask import Flask
from flask import abort
from flask import jsonify
from flask import redirect
from flask import request

ONE_WEEK_DURATION_IN_SECONDS = 7 * 24 * 60 * 60
SHORTENED_URL_LENGTH = 6
SHORTENED_URL_ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits


def create_app(redis_client=None):
    app = Flask(__name__)
    if redis_client is None:
        r = redis.StrictRedis()
    else:
        r = redis_client

    @app.route('/')
    def root():
        return generate_error_msg('Please use the /shorten_url endpoint to shorten a url')

    @app.route('/<shortened_url>', methods=['GET'])
    def get_shortened_url(shortened_url):
        original_url = r.get(shortened_url)
        if original_url is None:
            abort(404)
        return redirect(original_url, code=302)

    @app.route('/shorten_url', methods=['POST'])
    def shorten_url():
        is_valid, error_response = is_valid_post_request(request)

        if not is_valid:
            return error_response

        url = extract_url_from_request()
        key = generate_random_key()

        while r.get(key) is not None:
            key = generate_random_key()

        r.set(key, url, ONE_WEEK_DURATION_IN_SECONDS)
        return jsonify({'shortened_url': request.url_root + key}), 201

    def is_valid_post_request(request):
        # Make sure that the request header was set correctly and
        # that the request contains json body
        if not request.is_json or request.get_json(False, True, True) is None:
            return False, generate_error_msg('Your request should contain valid json body')

        url = extract_url_from_request()

        if url == '':
            return False, generate_error_msg('Please provide a url to be shortened')

        if not validators.url(url):
            return False, generate_error_msg('Please provide a valid url')

        return True, None

    def extract_url_from_request():
        return request.get_json().get('url', '')

    def generate_random_key():
        return ''.join(random.choices(SHORTENED_URL_ALPHABET, k=SHORTENED_URL_LENGTH))

    def generate_error_msg(msg):
        return jsonify({'error_message': msg}), 400

    return app
