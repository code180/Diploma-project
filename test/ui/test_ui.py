import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from main_page_ui import MainPage, ProductPage


@pytest.mark.ui
@allure.feature("Каталог")
def test_open_catalog():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    main_page = MainPage(driver)

    try:
        main_page.open()
        main_page.open_catalog()

        with allure.step("Проверка наличия товаров в каталоге"):
            search_result = main_page.get_search_results()
            assert len(search_result) > 0, "Товары найдены на странице"
    finally:
        driver.quit()


@pytest.mark.ui
@allure.feature("Поиск")
def test_search_for_book():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    main_page = MainPage(driver)

    try:
        main_page.open()
        main_page.search_for_book("Траун. Союзники")

        with allure.step("Проверка результатов поиска"):
            books = main_page.get_search_results()
            book_found = any(
                "Траун. Союзники" in book.find_element(By.CLASS_NAME, "product-card__title").text for book in books)
            assert book_found, "Книга 'Траун. Союзники' не найдена среди результатов поиска"
    finally:
        driver.quit()


@pytest.mark.ui
@allure.feature("Жанры")
def test_select_genre():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    main_page = MainPage(driver)

    try:
        main_page.open_genre_page()

        if not main_page.select_genre("Кулинария"):
            raise Exception("Элемент с текстом 'Кулинария' не найден")

        with allure.step("Проверка наличия книг в жанре 'Кулинария'"):
            books = main_page.get_genre_books()
            assert len(books) > 0, "На странице не найдено книг жанра 'Кулинария'"
    finally:
        driver.quit()


@pytest.mark.ui
@allure.feature("Корзина")
def test_add_book_to_cart():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    product_page = ProductPage(driver, "https://www.chitai-gorod.ru/product/traun-soyuzniki-2797027")

    try:
        product_page.open()
        product_page.add_to_cart()
        product_page.proceed_to_checkout()

        with allure.step("Проверка, что книга добавлена в корзину"):
            book_title = product_page.verify_book_in_cart()
            assert "Траун. Союзники" in book_title, "Книга не найдена в корзине"
    finally:
        driver.quit()


@pytest.mark.ui
@allure.feature("Корзина")
def test_add_and_remove_book_from_cart():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    product_page = ProductPage(driver, "https://www.chitai-gorod.ru/product/traun-soyuzniki-2797027")

    try:
        product_page.open()
        product_page.add_to_cart()
        product_page.proceed_to_checkout()

        with allure.step("Удаление книги из корзины"):
            return_text = product_page.remove_from_cart()
            assert return_text == "ВЕРНУТЬ В КОРЗИНУ", "Книга не удалена из корзины"
    finally:
        driver.quit()
