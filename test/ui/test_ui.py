from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def test_authorization():
    driver = webdriver.Chrome()
    driver.get("https://www.chitai-gorod.ru/")
    # Установка токена в cookie
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'header-profile__title'))
    )
    driver.add_cookie({
        'name': 'access-token',
        'value': 'Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIxMjM3MDY0LCJpYXQiOjE3MzE0MjQ0NTksImV4cCI6MTczMTQyODA1OSwidHlwZSI6MjB9.s0ftezZUVa2YoAdewAfESXhSS1q1IxCaKZ7OnCYGUGk',
        'domain': '.chitai-gorod.ru'
    })
    driver.refresh()  # Обновляем страницу, чтобы cookie применились
    header_profile = driver.find_element(
        By.CLASS_NAME, 'header-profile__title')
    assert header_profile.text == 'Александр'
