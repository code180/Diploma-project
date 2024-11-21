import pytest
import allure
from main_page_api import BooksAPI, CartAPI


@pytest.mark.api
def test_get_books():
    with allure.step("Тест на получение и проверку списка книг"):
        response = BooksAPI.get_books()

        assert response.status_code == 200
        books = response.json()
        products = books.get('data', {}).get('products', [])

        for product in products:
            with allure.step("Проверка наличия атрибутов у каждого продукта"):
                attributes = product.get('attributes', [])
                assert attributes, "Expected non-empty attributes list"


@pytest.mark.api
@allure.step("Тест на добавление товара в корзину")
def test_add_product_to_cart():
    with allure.step("Добавление продукта в корзину"):
        response = CartAPI.add_product_to_cart(2797027)
        assert response.status_code == 200

    with allure.step("Проверка наличия продукта в корзине"):
        response = CartAPI.get_cart_contents()
        assert response.status_code == 200

        response_json = response.json()
        assert "products" in response_json
        assert len(response_json["products"]) > 0


@pytest.mark.api
@allure.step("Тест на проверку наличия товара в корзине")
def test_check_cart_items():
    with allure.step("Проверка содержимого корзины"):
        response = CartAPI.get_cart_contents()
        assert response.status_code == 200

        response_json = response.json()
        assert "products" in response_json
        assert len(response_json["products"]) > 0


@pytest.mark.api
@allure.step("Тест на удаление продукта из корзины и проверку, что корзина пуста")
def test_remove_product_from_cart():
    with allure.step("Удаление продукта из корзины"):
        response = CartAPI.remove_product_from_cart(153888693)
        assert response.status_code in {200, 204}

    with allure.step("Проверка, что корзина пуста"):
        cart_response = CartAPI.get_cart_contents()
        assert cart_response.status_code == 200

        cart_response_json = cart_response.json()
        assert "products" in cart_response_json
        assert len(cart_response_json["products"]) == 0


@pytest.mark.api
@allure.step("Негативный тест: Проверка корзины без авторизации")
def test_check_cart_without_auth():
    with allure.step("Проверка содержимого корзины без авторизации"):
        response = CartAPI.get_cart_contents_without_auth()
        assert response.status_code == 401

        response_json = response.json()
        assert "message" in response_json
        assert response_json["message"] == "Authorization обязательное поле", "Сообщение об ошибке некорректное"
