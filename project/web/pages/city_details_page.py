from common.webdriver_qa_api.web.web_pages import WebPage
from selenium.webdriver.common.by import By
from common.webdriver_qa_api.web.web_elements import WebElement


class CityDetailsPage(WebPage):

    def __init__(self):
        super().__init__(By.XPATH, "//h2[text()='Current weather and forecasts in your city']", "City Details Page")
        self.lbl_pressure = WebElement(By.XPATH, "//td[text()='Pressure']/following-sibling::td[1]")
        self.lbl_humidity = WebElement(By.XPATH, "//td[text()='Humidity']/following-sibling::td[1]")
        self.lbl_sunrise = WebElement(By.XPATH, "//td[text()='Sunrise']/following-sibling::td[1]")
        self.lbl_sunset = WebElement(By.XPATH, "//td[text()='Sunset']/following-sibling::td[1]")