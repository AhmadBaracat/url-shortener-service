import fakeredis

from urlshortenerservice import create_app

SHORTEN_URL_ROUTE = '/shorten_url'


class TestUrlShortenerService:
    @classmethod
    def setup_class(cls):
        cls.r = fakeredis.FakeStrictRedis()
        cls.url_shortener_service = create_app(cls.r).test_client()

    def test_get_shortened_url_should_respond_with_404_if_key_is_not_in_datastore(self):
        response = self.url_shortener_service.get('key')
        assert response.status_code == 404

    def test_get_shortened_url_should_redirect_to_original_url(self):
        self.r.set('key', 'http://www.google.com')
        response = self.url_shortener_service.get('key')
        assert response.status_code == 302
        assert response.headers.get("Location") == 'http://www.google.com'

    def test_shorten_url_should_respond_with_400_if_header_content_type_is_not_set(self):
        response = self.url_shortener_service.post(SHORTEN_URL_ROUTE)
        assert response.status_code == 400

    def test_shorten_url_should_respond_with_400_if_url_is_not_set(self):
        response = self.url_shortener_service.post(SHORTEN_URL_ROUTE, json={})
        assert response.status_code == 400

    def test_shorten_url_should_respond_with_400_if_url_is_not_valid(self):
        response = self.url_shortener_service.post(SHORTEN_URL_ROUTE, json={'url': ''})
        assert response.status_code == 400

        response = self.url_shortener_service.post(SHORTEN_URL_ROUTE, json={'url': 'google.com'})
        assert response.status_code == 400

        response = self.url_shortener_service.post(SHORTEN_URL_ROUTE, json={'url': 'www.google.com'})
        assert response.status_code == 400

    def test_shorten_url_should_respond_with_201_if_url_is_valid(self):
        response = self.url_shortener_service.post(SHORTEN_URL_ROUTE, json={'url': 'http://www.google.com'})
        assert response.status_code == 201

    def test_shorten_url_response_should_contain_json_header_content_type(self):
        response = self.url_shortener_service.post(SHORTEN_URL_ROUTE, json={'url': 'http://www.google.com'})
        assert response.headers.get('Content-Type') == 'application/json'
