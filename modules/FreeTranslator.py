from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

class FreeTranslator:
    textAreaL = (By.XPATH, '//textarea[@aria-label="Texto de origem"]')
    textInTextAreaL = (By.CSS_SELECTOR, '.D5aOJc.vJwDU')
    responseL = (By.XPATH, '//span[@class="VIiyi"]')
    closeL = (By.XPATH, '//button[@aria-label="Limpar texto original"]')

    def __init__(self, url):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.url = url

    def open(self):
        self.driver.get(self.url)
    
    def close(self):
        self.driver.close()
    
    def getTextArea(self):
        self.textArea = self.driver.find_element(*self.textAreaL)

    def sendText(self, text):
        self.cleanTextArea()
        self.textArea.send_keys(text)
    
    def cleanTextArea(self):
        self.textInTextArea = self.driver.find_element(*self.textInTextAreaL).get_attribute('innerHTML')
        while self.textInTextArea:
            self.textArea.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
            self.textInTextArea = self.driver.find_element(*self.textInTextAreaL).get_attribute('innerHTML')

    def getResponse(self):
        self.translated = ""
        while self.translated == "":
            try:
                self.translated = self.driver.find_element(*self.responseL).text
            except (NoSuchElementException, StaleElementReferenceException, AttributeError):
                self.translated = ""
        return self.translated

    def resetText(self, nextText, lastResponse):
        self.sendText(nextText)

    def waitUntilLastResponseDisappear(self, lastResponse):
        newResponse = self.getResponse()
        while newResponse == lastResponse:
            newResponse = self.getResponse()