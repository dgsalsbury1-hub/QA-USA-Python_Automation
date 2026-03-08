import data
import helpers
from pages import UrbanRoutesPage
from selenium import webdriver


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def setup_method(self):
        """Run before each test: load the app fresh and create a new page object."""
        self.routes_page = UrbanRoutesPage(self.driver)
        self.routes_page.load(data.URBAN_ROUTES_URL)

    def test_set_routes(self):
        """Test that the from and to address fields are set correctly."""
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert self.routes_page.get_from() == data.ADDRESS_FROM, \
            f"FAIL: Expected from address '{data.ADDRESS_FROM}' but got '{self.routes_page.get_from()}'"
        assert self.routes_page.get_to() == data.ADDRESS_TO, \
            f"FAIL: Expected to address '{data.ADDRESS_TO}' but got '{self.routes_page.get_to()}'"

    def test_select_plan(self):
        """Test that the Supportive tariff plan is selected."""
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.select_supportive_plan()
        assert self.routes_page.is_supportive_plan_selected(), \
            "FAIL: Supportive plan was not selected"

    def test_fill_phone_number(self):
        """Test that the phone number is filled in and confirmed via SMS code."""
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.select_supportive_plan()
        self.routes_page.open_phone_modal()
        self.routes_page.enter_phone(data.PHONE_NUMBER)
        self.routes_page.click_next_phone()
        sms_code = helpers.retrieve_phone_code(self.driver)
        self.routes_page.enter_sms_code(sms_code)
        self.routes_page.confirm_phone()
        assert self.routes_page.is_phone_number_saved(data.PHONE_NUMBER), \
            f"FAIL: Phone number '{data.PHONE_NUMBER}' was not saved"

    def test_fill_card(self):
        """Test that a credit card can be added successfully."""
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.select_supportive_plan()
        self.routes_page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.routes_page.is_card_added(), \
            "FAIL: Credit card was not added to payment method"

    def test_comment_for_driver(self):
        """Test that a comment/message for the driver is entered correctly."""
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.select_supportive_plan()
        self.routes_page.enter_comment(data.MESSAGE_FOR_DRIVER)
        assert self.routes_page.get_comment() == data.MESSAGE_FOR_DRIVER, \
            f"FAIL: Expected comment '{data.MESSAGE_FOR_DRIVER}' but got '{self.routes_page.get_comment()}'"

    def test_order_blanket_and_handkerchiefs(self):
        """Test that the blanket and handkerchiefs toggle turns on, off, and back on."""
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.select_supportive_plan()
        self.routes_page.toggle_blanket()
        assert self.routes_page.is_blanket_ordered(), \
            "FAIL: Blanket should be ON after first toggle"
        self.routes_page.toggle_blanket()
        assert not self.routes_page.is_blanket_ordered(), \
            "FAIL: Blanket should be OFF after second toggle"
        self.routes_page.toggle_blanket()
        assert self.routes_page.is_blanket_ordered(), \
            "FAIL: Blanket should be ON after third toggle"

    def test_order_2_ice_creams(self):
        """Test that 2 ice creams are added to the order."""
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.select_supportive_plan()
        self.routes_page.order_ice_creams(2)
        assert self.routes_page.get_ice_cream_count() == 2, \
            f"FAIL: Expected 2 ice creams but got '{self.routes_page.get_ice_cream_count()}'"

    def test_car_search_model_appears(self):
        """Test that clicking Order Taxi shows the car search modal window."""
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.select_supportive_plan()
        self.routes_page.open_phone_modal()
        self.routes_page.enter_phone(data.PHONE_NUMBER)
        self.routes_page.click_next_phone()
        sms_code = helpers.retrieve_phone_code(self.driver)
        self.routes_page.enter_sms_code(sms_code)
        self.routes_page.confirm_phone()
        self.routes_page.enter_comment(data.MESSAGE_FOR_DRIVER)
        self.routes_page.click_order_taxi()
        assert self.routes_page.is_car_search_modal_visible(), \
            "FAIL: Car search modal did not appear after clicking Order Taxi"