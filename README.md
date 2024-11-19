# Тестовый проект для API и UI

## Описание задачи

Этот проект создан для автоматизации тестирования веб-приложения, включающего как API, так и UI тестирования. 
Цель проекта — обеспечить легкость и удобство в запуске тестов в различных режимах с использованием `pytest`.

## Структура проекта

  tests
    ├── api
    ├── test_api.py
    └── main_page_api.py
    │
    ├── ui
    │   ├── test_ui.py
    │   └── main_page_ui.py
    │
    ├── requirements.txt
    └── pytest.ini

### Компоненты

- **`main_page_api.py`**: Модуль для работы с API, содержит классы `BooksAPI` и `CartAPI` для управления запросами.
- **`main_page_ui.py`**: Модуль для работы с UI, содержит классы `MainPage` и `ProductPage`, использует Selenium для взаимодействия с браузером.
- **`test_api.py`**: Набор тестов для API, маркированных как `@pytest.mark.api`.
- **`test_ui.py`**: Набор тестов для UI, маркированных как `@pytest.mark.ui`.
  
## Установка

1. Установите Python (если еще не установлено).
2. Создайте и активируйте виртуальное окружение: python -m venv venv .\venv\Scripts\activate   # для Windows
3. Установите зависимости: pip install -r requirements.txt

## Запуск тестов

UI тесты: pytest -m ui
API тесты: pytest -m api
Все тесты: pytest

