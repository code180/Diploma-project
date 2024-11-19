import requests
import allure

BASE_URL = "https://web-gate.chitai-gorod.ru/api/"
TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIxMjM3MDY0LCJpYXQiOjE3MzE5Nzc3NzgsImV4cCI6MTczMTk4MTM3OCwidHlwZSI6MjB9.DEcuHmJQIQbHKat3P-4axHYeXDfI6FKCM38NHIuawa4"
HEADERS = {
    "Authorization": TOKEN,
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

class BooksAPI:
    @staticmethod
    @allure.step("Получение списка книг по фразе поиска")
    def get_books(phrase="Траун. Союзники") -> requests.Response:
        """Запрос списка книг по определенной фразе."""
        params = {
            "customerCityId": 213,
            "phrase": phrase,
            "products[page]": 1,
            "products[per-page]": 48,
            "sortPreset": "relevance"
        }
        response = requests.get(f"{BASE_URL}v2/search/product", headers=HEADERS, params=params)
        return response


class CartAPI:
    @staticmethod
    @allure.step("Добавление товара в корзину")
    def add_product_to_cart(product_id: int) -> requests.Response:
        payload = {
            "id": product_id,
            "adData": {
                "item_list_name": "search",
                "product_shelf": ""
            }
        }
        return requests.post(f"{BASE_URL}v1/cart/product", headers=HEADERS, json=payload)

    @staticmethod
    @allure.step("Получение содержимого корзины")
    def get_cart_contents() -> requests.Response:
        return requests.get(f"{BASE_URL}v1/cart", headers=HEADERS)

    @staticmethod
    @allure.step("Удаление товара из корзины")
    def remove_product_from_cart(product_id: int) -> requests.Response:
        return requests.delete(f"{BASE_URL}v1/cart/product/{product_id}", headers=HEADERS)

    @staticmethod
    @allure.step("Получение содержимого корзины без авторизации")
    def get_cart_contents_without_auth() -> requests.Response:
        headers_no_auth = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        return requests.get(f"{BASE_URL}v1/cart", headers=headers_no_auth)
