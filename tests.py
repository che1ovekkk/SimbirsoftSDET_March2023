import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import allure


@allure.step('Открываем браузер')
def open_browser(url):
    browser = webdriver.Chrome()
    browser.get(url=url)
    browser.implicitly_wait(3)
    return browser


@allure.title('Кейс 1. Проверка успешной покупки')
def test_case_1():
    browser = open_browser(url='https://www.saucedemo.com')
    with allure.step('Ищем поле для ввода логина'):
        login_field = browser.find_element(By.CSS_SELECTOR, '.input_error')

    with allure.step('Отправляем логин'):
        login_field.send_keys('standard_user')
    login_field.send_keys(Keys.RETURN)

    with allure.step('Ищем поле для ввода пароля'):
        password_field = browser.find_element(By.ID, 'password')

    with allure.step('Отправляем пароль'):
        # you shouldn't do like this - it's better to hide pass in other file and import it
        password_field.send_keys('secret_sauce')
    password_field.send_keys(Keys.RETURN)

    with allure.step('Ищем кнопку входа'):
        login_button = browser.find_element(By.XPATH, '//*[@id="login-button"]')
        with allure.step('Нажимаем кнопку входа'):
            login_button.click()

    with allure.step('Переходим на страницу товаров'):
        time.sleep(1)

    with allure.step('Добавляем товар в корзину'):
        first_add_to_card = browser.find_element(By.ID, 'add-to-cart-sauce-labs-backpack')
        first_add_to_card.click()

    with allure.step('Переходим в корзину'):
        card_icon = browser.find_element(By.CLASS_NAME, 'shopping_cart_link')
        card_icon.click()

    with allure.step('Ищем кнопку "CHECKOUT"'):
        checkout_button = browser.find_element(By.ID, 'checkout')
        checkout_button.click()

    with allure.step('Ищем поле "First Name"'):
        first_name_field = browser.find_element(By.ID, 'first-name')
        with allure.step('Заполняем поле "First Name"'):
            first_name_field.send_keys('test')

    with allure.step('Ищем поле "Last Name"'):
        last_name_field = browser.find_element(By.ID, 'last-name')
        with allure.step('Заполняем поле "Last Name"'):
            last_name_field.send_keys('test')

    with allure.step('Ищем поле "Zip Code"'):
        zip_code_field = browser.find_element(By.ID, 'postal-code')
        with allure.step('Заполняем поле "Zip Code"'):
            zip_code_field.send_keys('test')

    with allure.step('Нажимаем кнопку "Continue"'):
        continue_button = browser.find_element(By.ID, 'continue')
        continue_button.click()

    with allure.step('Нажимаем кнопку "FINISH"'):
        finish_button = browser.find_element(By.ID, 'finish')
        browser.execute_script("arguments[0].scrollIntoView();", finish_button)
        finish_button.click()

    final_url = browser.current_url
    h2 = browser.find_element(By.CLASS_NAME, 'complete-header').text
    expected_url = 'https://www.saucedemo.com/checkout-complete.html'
    expected_message = 'THANK YOU FOR YOUR ORDER'

    assert final_url == expected_url
    assert h2 == expected_message


@allure.title('Кейс 2. Проверка сообщения об ошибке при попытке ввода логина на несуществующего пользователя')
def test_case_2():
    browser = open_browser(url='https://www.saucedemo.com')
    with allure.step('Ищем поле для ввода логина'):
        login_field = browser.find_element(By.CSS_SELECTOR, '.input_error')

    with allure.step('Отправляем логин'):
        login_field.send_keys('test')
    login_field.send_keys(Keys.RETURN)

    with allure.step('Ищем поле для ввода пароля'):
        password_field = browser.find_element(By.ID, 'password')

    with allure.step('Отправляем пароль'):
        # you shouldn't do like this - it's better to hide pass in other file and import it
        password_field.send_keys('test')
    password_field.send_keys(Keys.RETURN)

    with allure.step('Ищем кнопку входа'):
        login_button = browser.find_element(By.XPATH, '//*[@id="login-button"]')
        with allure.step('Нажимаем кнопку входа'):
            login_button.click()

    h3 = browser.find_element(By.TAG_NAME, 'h3').text
    expected_message = 'Epic sadface: Username and password do not match any user in this service'
    assert h3 == expected_message


"""To generate allure report we need:
* In terminal: pytest -v tests.py --alluredir=/tmp/my_allure_results
* In PowerShell: allure serve /tmp/my_allure_results"
"""
