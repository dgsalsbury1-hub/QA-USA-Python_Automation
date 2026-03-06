import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class UrbanRoutesPage:

    # --- Locators ---

    # Address fields
    FROM_FIELD = (By.ID, 'from')
    TO_FIELD = (By.ID, 'to')

    # Route type picker - click Fastest to reveal tariff cards
    FASTEST_BUTTON = (By.XPATH, "//div[contains(@class,'type-picker')]//div[text()='Fastest']")

    # Call a taxi button
    CALL_TAXI_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')

    # Supportive tariff card icon
    SUPPORTIVE_PLAN = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]/div[1]/img')

    # Active state check for Supportive
    SUPPORTIVE_PLAN_ACTIVE = (By.XPATH,
        "//div[contains(@class,'tcard') and contains(@class,'active')]"
        "[.//div[@class='tcard-title' and text()='Supportive']]"
    )

    # Phone number
    PHONE_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/div')
    PHONE_INPUT = (By.ID, 'phone')
    PHONE_NEXT_BUTTON = (By.XPATH, "//button[text()='Next']")
    SMS_CODE_INPUT = (By.ID, 'code')
    SMS_CONFIRM_BUTTON = (By.XPATH, "//button[text()='Confirm']")

    # Payment method
    PAYMENT_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[1]')
    ADD_CARD_OPTION = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[3]/div')
    CARD_NUMBER_INPUT = (By.XPATH, '//*[@id="number"]')
    CARD_CVV_INPUT = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[2]/div/input[@id="code"]')
    CARD_FORM = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form')
    CARD_LINK_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    PAYMENT_CLOSE_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    CARD_ADDED_TEXT = (By.XPATH, "//div[contains(@class,'pp-value-text')]")

    # Driver comment
    DRIVER_COMMENT = (By.XPATH, '//*[@id="comment"]')

    # Blanket and handkerchiefs
    BLANKET_TOGGLE = (By.XPATH,
        '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span'
    )
    BLANKET_INPUT = (By.XPATH,
        "//div[contains(@class,'r-sw')]"
        "[.//div[contains(text(),'Blanket') or contains(text(),'blanket')]]"
        "//input[@type='checkbox']"
    )

    # Ice cream
    ICE_CREAM_PLUS = (By.XPATH,
        '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]'
    )
    ICE_CREAM_VALUE = (By.XPATH,
        "//div[contains(text(),'Ice cream')]"
        "/following::div[contains(@class,'counter-value')][1]"
    )

    # Order button and car search modal
    ORDER_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button/span[1]')
    CAR_SEARCH_MODAL = (By.XPATH,
        "//div[contains(@class,'order-header-title') and contains(text(),'Look')]"
        " | //div[contains(@class,'searching')]"
        " | //div[@class='order-body']"
    )

    # Overlay element
    OVERLAY = (By.XPATH, "//div[@class='overlay']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def _js_click(self, locator):
        """Use JavaScript to click an element, bypassing any overlay blocking it."""
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def _dismiss_overlay(self):
        """If an overlay is present, click it to dismiss it."""
        try:
            overlay = self.driver.find_element(*self.OVERLAY)
            if overlay.is_displayed():
                self.driver.execute_script("arguments[0].click();", overlay)
                time.sleep(0.5)
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Page load
    # -------------------------------------------------------------------------

    def load(self, url):
        self.driver.get(url)

    # -------------------------------------------------------------------------
    # 1. Address
    # -------------------------------------------------------------------------

    def set_from(self, address):
        field = self.wait.until(EC.element_to_be_clickable(self.FROM_FIELD))
        field.clear()
        field.send_keys(address)

    def set_to(self, address):
        field = self.wait.until(EC.element_to_be_clickable(self.TO_FIELD))
        field.clear()
        field.send_keys(address)

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def get_from(self):
        return self.driver.find_element(*self.FROM_FIELD).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.TO_FIELD).get_property('value')

    # -------------------------------------------------------------------------
    # 2. Supportive plan
    # -------------------------------------------------------------------------

    def select_supportive_plan(self):
        """
        Full tariff selection flow:
          1. Click Fastest route type button
          2. Click 'Call a taxi' button
          3. Click Supportive tariff icon - only if not already active
        """
        fastest = self.wait.until(EC.element_to_be_clickable(self.FASTEST_BUTTON))
        fastest.click()

        call_taxi = self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON))
        call_taxi.click()

        self.wait.until(EC.presence_of_element_located(self.SUPPORTIVE_PLAN))
        if not self.is_supportive_plan_selected():
            self._js_click(self.SUPPORTIVE_PLAN)

    def is_supportive_plan_selected(self):
        active = self.driver.find_elements(*self.SUPPORTIVE_PLAN_ACTIVE)
        return len(active) > 0

    # -------------------------------------------------------------------------
    # 3. Phone number
    # -------------------------------------------------------------------------

    def open_phone_modal(self):
        self._dismiss_overlay()
        self._js_click(self.PHONE_BUTTON)

    def enter_phone(self, phone):
        field = self.wait.until(EC.element_to_be_clickable(self.PHONE_INPUT))
        field.clear()
        field.send_keys(phone)

    def click_next_phone(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.PHONE_NEXT_BUTTON))
        btn.click()

    def enter_sms_code(self, code):
        """Enter the SMS code retrieved from helpers.retrieve_phone_code()."""
        field = self.wait.until(EC.element_to_be_clickable(self.SMS_CODE_INPUT))
        field.clear()
        field.send_keys(code)

    def confirm_phone(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.SMS_CONFIRM_BUTTON))
        btn.click()
        time.sleep(1)

    # -------------------------------------------------------------------------
    # 4. Credit card
    # -------------------------------------------------------------------------

    def open_payment_modal(self):
        self._dismiss_overlay()
        self._js_click(self.PAYMENT_BUTTON)

    def click_add_card(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_OPTION))
        btn.click()

    def enter_card_number(self, number):
        field = self.wait.until(EC.element_to_be_clickable(self.CARD_NUMBER_INPUT))
        field.clear()
        field.send_keys(number)

    def enter_cvv(self, code):
        """Enter CVV using JavaScript to set value, then click form to lose focus."""
        # Wait until we are inside the card modal
        self.wait.until(EC.presence_of_element_located(self.CARD_NUMBER_INPUT))
        # Use JS to fill the CVV field by id='code' and class='card-input'
        self.driver.execute_script("""
            var field = document.querySelector('input#code.card-input');
            if (field) {
                field.focus();
                var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(field, arguments[0]);
                field.dispatchEvent(new Event('input', { bubbles: true }));
                field.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """, code)
        # Click the form to trigger focus loss and enable the Link button
        form = self.driver.find_element(*self.CARD_FORM)
        form.click()

    def click_link(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CARD_LINK_BUTTON))
        btn.click()

    def close_payment_modal(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_CLOSE_BUTTON))
        btn.click()
        time.sleep(1)

    def add_credit_card(self, number, code):
        self.open_payment_modal()
        self.click_add_card()
        self.enter_card_number(number)
        self.enter_cvv(code)
        self.click_link()
        self.close_payment_modal()

    def is_card_added(self):
        els = self.driver.find_elements(*self.CARD_ADDED_TEXT)
        return len(els) > 0

    # -------------------------------------------------------------------------
    # 5. Driver comment
    # -------------------------------------------------------------------------

    def enter_comment(self, comment):
        field = self.wait.until(EC.element_to_be_clickable(self.DRIVER_COMMENT))
        field.clear()
        field.send_keys(comment)

    def get_comment(self):
        return self.driver.find_element(*self.DRIVER_COMMENT).get_property('value')

    # -------------------------------------------------------------------------
    # 6. Blanket and handkerchiefs
    # -------------------------------------------------------------------------

    def order_blanket_and_handkerchiefs(self):
        """
        Two separate selectors per project brief:
        - BLANKET_TOGGLE to click (the visible span toggle)
        - BLANKET_INPUT  to assert (the hidden checkbox state)
        """
        self._dismiss_overlay()
        checkbox = self.wait.until(EC.presence_of_element_located(self.BLANKET_INPUT))
        if not checkbox.is_selected():
            self._js_click(self.BLANKET_TOGGLE)

    def is_blanket_ordered(self):
        checkbox = self.driver.find_element(*self.BLANKET_INPUT)
        return checkbox.is_selected()

    # -------------------------------------------------------------------------
    # 7. Ice cream
    # -------------------------------------------------------------------------

    def add_ice_cream(self):
        self._dismiss_overlay()
        self._js_click(self.ICE_CREAM_PLUS)

    def order_ice_creams(self, quantity):
        """Loop lives in pages.py per project brief."""
        for _ in range(quantity):
            self.add_ice_cream()

    def get_ice_cream_count(self):
        el = self.driver.find_element(*self.ICE_CREAM_VALUE)
        return int(el.text)

    # -------------------------------------------------------------------------
    # 8. Order taxi
    # -------------------------------------------------------------------------

    def click_order_taxi(self):
        self._dismiss_overlay()
        self._js_click(self.ORDER_BUTTON)
        time.sleep(21)

    def is_car_search_modal_visible(self):
        try:
            modal = self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))
            return modal.is_displayed()
        except Exception:
            return False