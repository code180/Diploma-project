from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_open_catalog():
    """Тест на открытие каталога книг."""
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.chitai-gorod.ru/")
    driver.maximize_window

    driver.find_element(By.CLASS_NAME, "catalog__button").click()
    driver.find_element(By.XPATH, '//span[text()="Книги"]').click()
    driver.find_element(
        By.XPATH, '//a[text()="Посмотреть все товары"]').click()
    search_result = driver.find_elements(
        By.CLASS_NAME, "product-card product-card product")
    assert len(search_result) > 0
    driver.quit()


def test_select_genre():
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.chitai-gorod.ru/catalog/books-18030")
    driver.maximize_window

    """Тест на выбор жанра книг."""
    genre_links = driver.find_elements(
        By.CLASS_NAME, 'catalog-menu__parent--children')
    for link in genre_links:
        if link.text == 'Кулинария':
            link.click()
            break
    else:
        raise Exception("Элемент с текстом 'Кулинария' не найден")
    assert "Кулинария" in driver.page_source
    driver.quit()


def test_search_for_book(driver):
    """Тест на поиск книги."""
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.chitai-gorod.ru/")
    driver.maximize_window

    search_box = driver.find_element(By.CLASS_NAME, 'header-search__input')
    search_box.send_keys("Траун. Союзники")
    search_box.submit()
    assert driver.find_element(
        By.CLASS_NAME, 'result-item__mark').is_displayed()
    driver.quit()


def test_add_book_to_cart(driver):
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
    driver.get(
        "https://www.chitai-gorod.ru/search?phrase=%D0%A2%D1%80%D0%B0%D1%83%D0%BD.%20%D0%A1%D0%BE%D1%8E%D0%B7%D0%BD%D0%B8%D0%BA%D0%B8")

    """Тест на добавление книги в корзину."""
    # Ожидание, пока появится элемент книги "Траун. Союзники"
    book_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, "//div[@data-chg-product-name='Траун. Союзники']"))
    )
    # Поиск кнопки "Купить" в рамках блока с книгой
    buy_button = book_element.find_element(
        By.XPATH, ".//div[contains(@class, 'button action-button blue')]")
    # Клик по кнопке "Купить"
    buy_button.click()

    cart_items = driver.find_element(By.CLASS_NAME, "action-button__text")

    assert "Оформить" in cart_items.text
    driver.quit()

def test_add_book_to_bookmarks():
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.chitai-gorod.ru/search?phrase=%D0%A2%D1%80%D0%B0%D1%83%D0%BD.%20%D0%A1%D0%BE%D1%8E%D0%B7%D0%BD%D0%B8%D0%BA%D0%B8")

    # Ожидание появления блока с книгой "Траун. Союзники"
    book_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, "//div[@data-chg-product-name='Траун. Союзники']"))
    )

    # Поиск кнопки "Закладки" в рамках блока книги
    book_element.find_element(
        By.XPATH, ".//button[contains(@class, 'button favorite-button')]").click()

    bookmarks = driver.find_element(
        By.CLASS_NAME, "badge-notice header-bookmarks__badge")
    assert "1" in bookmarks.text
    driver.quit()
