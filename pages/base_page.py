from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .locators import BasePageLocators

class BasePage():
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(10)

    def go_to_login_page(self):
        link = self.browser.find_element(*BasePageLocators.LOGIN_LINK)
        link.click()

    def should_be_login_link(self):
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Ссылка на страницу авторизаци не найдена"
        
    def open(self):
        self.browser.get(self.url)

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except (NoSuchElementException):
            return False
        return True

    def try_click_element(self, how, what):
        try:
            self.browser.find_element(how,what).click()
        except (NoSuchElementException):
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    def is_disappeared(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException).\
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    def go_to_cart(self):
        link = self.browser.find_element(*BasePageLocators.GO_TO_CART_BUTTON)
        link.click()

    def cart_list_is_empty(self):
        elements = self.browser.find_elements(*BasePageLocators.CART_ITEMS_ROWS)
        assert len(elements) == 0, "Корзина оказалась не пустой"

    def cart_is_empty_message(self):
        assert self.is_element_present(*BasePageLocators.EMPTY_CART_MESSAGE), "Сообщения о пустой корзине нет"