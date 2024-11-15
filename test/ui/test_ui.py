from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def test_add_book_to_cart():
    # Запуск браузера
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Переход на страницу книги
    driver.get("https://www.chitai-gorod.ru/product/traun-soyuzniki-2797027")
    driver.maximize_window()

    # Ожидание появления кнопки "Купить"
    buy_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, ".//button[contains(@class, 'product-offer-button chg-app-button chg-app-button--primary chg-app-button--extra-large chg-app-button--brand-blue chg-app-button--block')]"))
    )

    # Клик по кнопке "Купить"
    buy_button.click()

    # Ожидание появления кнопки "Оформить"
    offer_button = WebDriverWait(driver, 10).until(
         EC.presence_of_element_located(
            (By.CLASS_NAME, 'product-offer-button chg-app-button chg-app-button--primary chg-app-button--extra-large chg-app-button--green chg-app-button--block'))
    )

    # Нажатие на кнопку "Оформить"
    offer_button.click()

    # Ожидание загрузки корзины
    cart_items = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "products__items")))

    # Проверка, что книга "Траун. Союзники" есть в корзине
    book = cart_items.find_element(By.CLASS_NAME, "product-title__head")
    assert book.text == "Траун. Союзники"

    # Завершаем работу браузера
    driver.quit()

