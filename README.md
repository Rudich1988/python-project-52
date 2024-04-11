### Hexlet tests and linter status:
[![Actions Status](https://github.com/Rudich1988/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Rudich1988/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/aceb29e3373cdf276005/maintainability)](https://codeclimate.com/github/Rudich1988/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/aceb29e3373cdf276005/test_coverage)](https://codeclimate.com/github/Rudich1988/python-project-52/test_coverage)


## Проект Менеджер задач:
[Менеджер задач](https://djangoapp-h53n.onrender.com) - это система управления задачами. Она позволяет ставить задачи, назначать исполнителей и менять их статусы.


### Как развернуть проект:
- Создайте в корне проекта файл .env
- Создайте переменную SECRET_KEY в .env файле
- Создайте переменную POST_SERVER_ITEM_ACCESS_TOKEN, значением которой будет значение Server-side access token в Вашем Rollbar
- Если Вы не хотите использовать дефолтную базу данных sqlite3, Вы можете создать переменную DATABASE_URL, которая будет содержать путь к Вашей базе данных
- Далее:

```python
poetry install
poetry shell
```

- Сделайте экспорт переменных, находящихся в файле .env:

```python
export {veriable}={veriable_value}
```

- Для запуска запуска проекта используйте команду:
```python
make dev
```