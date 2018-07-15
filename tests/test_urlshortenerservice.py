from urlshortenerservice import app

SHORTEN_URL_ROUTE = '/shorten_url'


class TestUrlShortenerService:
    @classmethod
    def setup_class(cls):
        cls.url_shortener_service = app.test_client()

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
