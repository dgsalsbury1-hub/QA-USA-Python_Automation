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
    # Assertion: phone number saved - the phone button text updates to show the number
    PHONE_NUMBER_SAVED = (By.XPATH,
        '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/div'
    )

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
    # BLANKET_TOGGLE -> click to activate
    # BLANKET_INPUT  -> assert state (hidden checkbox)
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
    CAR_SEARCH_MODAL = (By.XPATH, "//div[@class='order-body']")

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
        time.sleep(2)

    def set_to(self, address):
        field = self.wait.until(EC.element_to_be_clickable(self.TO_FIELD))
        field.clear()
        field.send_keys(address)
        time.sleep(2)

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
             (if condition per project brief to avoid double-clicks)
        """
        fastest = self.wait.until(EC.element_to_be_clickable(self.FASTEST_BUTTON))
        fastest.click()
        time.sleep(2)

        call_taxi = self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON))
        call_taxi.click()
        time.sleep(2)

        self.wait.until(EC.presence_of_element_located(self.SUPPORTIVE_PLAN))
        if not self.is_supportive_plan_selected():
            self._js_click(self.SUPPORTIVE_PLAN)
        time.sleep(2)

    def is_supportive_plan_selected(self):
        """Returns True if the active tariff card text matches 'Supportive'."""
        try:
            active = self.driver.find_elements(*self.SUPPORTIVE_PLAN_ACTIVE)
            if active:
                title = active[0].find_element(By.XPATH, ".//div[@class='tcard-title']")
                return title.text == 'Supportive'
            return False
        except Exception:
            return False

    # -------------------------------------------------------------------------
    # 3. Phone number
    # -------------------------------------------------------------------------

    def open_phone_modal(self):
        self._dismiss_overlay()
        self._js_click(self.PHONE_BUTTON)
        time.sleep(2)

    def enter_phone(self, phone):
        field = self.wait.until(EC.element_to_be_clickable(self.PHONE_INPUT))
        field.clear()
        field.send_keys(phone)
        time.sleep(2)

    def click_next_phone(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.PHONE_NEXT_BUTTON))
        btn.click()
        time.sleep(2)

    def enter_sms_code(self, code):
        """Enter the SMS code retrieved from helpers.retrieve_phone_code()."""
        field = self.wait.until(EC.element_to_be_clickable(self.SMS_CODE_INPUT))
        field.clear()
        field.send_keys(code)
        time.sleep(2)

    def confirm_phone(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.SMS_CONFIRM_BUTTON))
        btn.click()
        time.sleep(2)

    def is_phone_number_saved(self, phone):
        """Returns True if the phone button text matches the expected phone number."""
        try:
            el = self.wait.until(EC.presence_of_element_located(self.PHONE_NUMBER_SAVED))
            return el.text.strip() == phone
        except Exception:
            return False

    # -------------------------------------------------------------------------
    # 4. Credit card
    # -------------------------------------------------------------------------

    def open_payment_modal(self):
        self._dismiss_overlay()
        self._js_click(self.PAYMENT_BUTTON)
        time.sleep(2)

    def click_add_card(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_OPTION))
        btn.click()
        time.sleep(2)

    def enter_card_number(self, number):
        field = self.wait.until(EC.element_to_be_clickable(self.CARD_NUMBER_INPUT))
        field.clear()
        field.send_keys(number)
        time.sleep(2)

    def enter_cvv(self, code):
        """Enter CVV using JavaScript to set value, then click form to lose focus."""
        self.wait.until(EC.presence_of_element_located(self.CARD_NUMBER_INPUT))
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
        form = self.driver.find_element(*self.CARD_FORM)
        form.click()
        time.sleep(2)

    def click_link(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CARD_LINK_BUTTON))
        btn.click()
        time.sleep(2)

    def close_payment_modal(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_CLOSE_BUTTON))
        btn.click()
        time.sleep(2)

    def add_credit_card(self, number, code):
        self.open_payment_modal()
        self.click_add_card()
        self.enter_card_number(number)
        self.enter_cvv(code)
        self.click_link()
        self.close_payment_modal()

    def is_card_added(self):
        """Returns True if payment method text equals 'Card'."""
        try:
            el = self.wait.until(EC.presence_of_element_located(self.CARD_ADDED_TEXT))
            return el.text.strip() == 'Card'
        except Exception:
            return False

    # -------------------------------------------------------------------------
    # 5. Driver comment
    # -------------------------------------------------------------------------

    def enter_comment(self, comment):
        field = self.wait.until(EC.element_to_be_clickable(self.DRIVER_COMMENT))
        field.clear()
        field.send_keys(comment)
        time.sleep(2)

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

    def toggle_blanket(self):
        """Click the blanket toggle unconditionally, pausing 2 seconds before and after."""
        self._dismiss_overlay()
        self.wait.until(EC.presence_of_element_located(self.BLANKET_INPUT))
        time.sleep(2)
        self._js_click(self.BLANKET_TOGGLE)
        time.sleep(2)

    def is_blanket_ordered(self):
        """Returns True if blanket and handkerchiefs checkbox is checked."""
        checkbox = self.driver.find_element(*self.BLANKET_INPUT)
        return checkbox.get_property('checked')

    # -------------------------------------------------------------------------
    # 7. Ice cream
    # -------------------------------------------------------------------------

    def add_ice_cream(self):
        self._dismiss_overlay()
        self._js_click(self.ICE_CREAM_PLUS)
        time.sleep(2)

    def order_ice_creams(self, quantity):
        """Loop lives in pages.py per project brief."""
        for _ in range(quantity):
            self.add_ice_cream()

    def get_ice_cream_count(self):
        """Returns the current ice cream counter value as an integer."""
        el = self.driver.find_element(*self.ICE_CREAM_VALUE)
        return int(el.text)

    # -------------------------------------------------------------------------
    # 8. Order taxi
    # -------------------------------------------------------------------------

    def click_order_taxi(self):
        self._dismiss_overlay()
        self._js_click(self.ORDER_BUTTON)
        time.sleep(32)

    def is_car_search_modal_visible(self):
        """Returns True if the car search modal is displayed, False otherwise."""
        try:
            modal = self.wait.until(EC.presence_of_element_located(self.CAR_SEARCH_MODAL))
            return modal.is_displayed()
        except Exception:
            return False

    def wait_for_order_confirmation(self):
        """Dynamically waits up to 3 minutes for the order confirmation to appear."""
        try:
            confirm_wait = WebDriverWait(self.driver, 180)
            confirm_wait.until(lambda d: d.execute_script("""
                var el = document.querySelector('.order-header-title');
                return el && el.innerText && el.innerText.trim().length > 0;
            """))
            return True
        except Exception:
            return False