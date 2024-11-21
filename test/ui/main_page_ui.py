import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.chitai-gorod.ru/"

    def open(self):
        with allure.step("Открытие главной страницы"):
            self.driver.get(self.url)
            self.driver.maximize_window()

    def open_genre_page(self):
        genre_page_url = "https://www.chitai-gorod.ru/catalog/books-18030"
        with allure.step("Открытие страницы жанра 'Кулинария'"):
            self.driver.get(genre_page_url)
            self.driver.maximize_window()

    def open_catalog(self):
        with allure.step("Открытие каталога"):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "catalog__button"))
            ).click()

    def search_for_book(self, book_name):
        with allure.step(f"Поиск книги по названию: {book_name}"):
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "header-search__input"))
            )
            search_box.send_keys(book_name)
            search_button = self.driver.find_element(By.CLASS_NAME, "header-search__button")
            search_button.click()

    def get_search_results(self):
        with allure.step("Получение результатов поиска"):
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card"))
            )

    def select_genre(self, genre_name):
        with allure.step(f"Выбор жанра: {genre_name}"):
            genre_links = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "catalog-menu__parent--children"))
            )

            for link in genre_links:
                if link.text.strip() == genre_name:
                    link.click()
                    return True
            return False

    def get_genre_books(self):
        with allure.step("Получение книг выбранного жанра"):
            return WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card"))
            )

class ProductPage:
    def __init__(self, driver, book_url):
        self.driver = driver
        self.url = book_url

    def open(self):
        with allure.step("Открытие страницы книги"):
            self.driver.get(self.url)
            self.driver.maximize_window()

    def add_to_cart(self):
        with allure.step("Добавление книги в корзину"):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, ".//button[contains(@class, 'product-offer-button chg-app-button chg-app-button--primary chg-app-button--extra-large chg-app-button--brand-blue chg-app-button--block')]")
                )
            ).click()

    def proceed_to_checkout(self):
        with allure.step("Переход к оформлению заказа"):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, ".//button[contains(@class, 'product-offer-button chg-app-button chg-app-button--primary chg-app-button--extra-large chg-app-button--green chg-app-button--block')]")
                )
            ).click()

    def verify_book_in_cart(self):
        with allure.step("Проверка наличия книги в корзине"):
            cart_items = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "products__items"))
            )
            book = cart_items.find_element(By.CLASS_NAME, "product-title__head")
            return book.text

    def remove_from_cart(self):
        with allure.step("Удаление книги из корзины"):
            cart_items = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "products__items"))
            )
            remove_button = cart_items.find_element(By.XPATH, ".//button[contains(@class, 'button cart-item__actions-button cart-item__actions-button--delete light-blue')]")
            remove_button.click()
            return_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "item-removed__actions-button"))
            )
            return return_button.text
