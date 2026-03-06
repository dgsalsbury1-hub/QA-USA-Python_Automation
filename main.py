import data
import helpers
from pages import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Check active server status before testing
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

        # Load the app and create the page object shared across all tests
        cls.routes_page = UrbanRoutesPage(cls.driver)
        cls.routes_page.load(data.URBAN_ROUTES_URL)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_set_routes(self):
        """Test that the from and to address fields are set correctly."""
        self.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert self.routes_page.get_from() == data.ADDRESS_FROM
        assert self.routes_page.get_to() == data.ADDRESS_TO

    def test_select_plan(self):
        """Test that the Supportive tariff plan is selected."""
        self.routes_page.select_supportive_plan()
        assert self.routes_page.is_supportive_plan_selected(), "Supportive plan was not selected"

    def test_fill_phone_number(self):
        """Test that the phone number is filled in and confirmed via SMS code."""
        self.routes_page.open_phone_modal()
        self.routes_page.enter_phone(data.PHONE_NUMBER)
        self.routes_page.click_next_phone()
        # Retrieve the SMS code using the helper after the request has been made
        sms_code = helpers.retrieve_phone_code(self.driver)
        self.routes_page.enter_sms_code(sms_code)
        self.routes_page.confirm_phone()

    def test_fill_card(self):
        """Test that a credit card can be added successfully."""
        self.routes_page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.routes_page.is_card_added(), "Credit card was not added to payment method"

    def test_comment_for_driver(self):
        """Test that a comment/message for the driver is entered correctly."""
        self.routes_page.enter_comment(data.MESSAGE_FOR_DRIVER)
        assert self.routes_page.get_comment() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        """Test that the blanket and handkerchiefs option is toggled on."""
        self.routes_page.order_blanket_and_handkerchiefs()
        # Assert using the checkbox input (state selector), not the slider label (click selector)
        assert self.routes_page.is_blanket_ordered(), "Blanket and handkerchiefs were not ordered"

    def test_order_2_ice_creams(self):
        """Test that 2 ice creams are added to the order."""
        self.routes_page.order_ice_creams(2)
        assert self.routes_page.get_ice_cream_count() == 2, "Ice cream count is not 2"

    def test_car_search_model_appears(self):
        """Test that clicking Order Taxi shows the car search modal window."""
        self.routes_page.click_order_taxi()
        assert self.routes_page.is_car_search_modal_visible(), "Car search modal did not appear"