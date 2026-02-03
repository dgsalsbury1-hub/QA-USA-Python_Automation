import data
import helpers

print(data.URBAN_ROUTES_URL)
print(data.ADDRESS_FROM)


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Task 4: Check active server status before testing
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    # Task 3:  Test functions for Urban Routes ordering process
    def test_set_routes(self):
        # Add in S8
        print("function created for set route")
        pass

    def test_select_plan(self):
        # Add in S8
        print("function created for select plan")
        pass

    def test_fill_phone_number(self):
        # Add in S8
        print("function created for fill phone number")
        pass

    def test_fill_card(self):
        # Add in S8
        print("function created for fill card")
        pass

    def test_comment_for_driver(self):
        # Add in S8
        print("function created for comment for driver")
        pass

    def test_order_blanket_and_handkerchiefs(self):
        # Add in S8
        print("function created for order blanket and handkerchiefs")
        pass

    # Task 5: Adding a for loop
    def test_order_2_ice_creams(self):
        # Add in S8
        print("function created for order 2 ice creams")
        for i in range(2):
            # Add in S8
            pass

    def test_car_search_model_appears(self):
        # Add in S8
        print("function created for car search model appears")
        pass
