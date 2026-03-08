# Test Summary Report

![Python](https://img.shields.io/badge/Python-3.14.2-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.25.0-green?logo=selenium)
![Chrome](https://img.shields.io/badge/Chrome-145.0.7632-orange?logo=googlechrome)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-lightgrey?logo=windows)
![Tests](https://img.shields.io/badge/Tests-8%20Passed-brightgreen?logo=pytest)
![GitHub](https://img.shields.io/badge/GitHub-Repo-black?logo=github)
![GitLab](https://img.shields.io/badge/GitLab-Repo-orange?logo=gitlab)

---

## Project Name
Urban Routes UI Automation — Sprint 8 End-to-End Test Suite

---

## Scope

### What Was Tested
- Route entry (from and to address fields)
- Supportive tariff plan selection
- Phone number entry and SMS code confirmation
- Credit card payment method entry and verification
- Driver comment/message input
- Blanket and handkerchiefs toggle (on/off/on cycle)
- Ice cream counter (2 items via loop)
- Full taxi order flow triggering the car search modal

### What Was NOT Tested
- Negative/invalid input scenarios (e.g., wrong phone format, invalid card)
- Other tariff plans (Express, Business, etc.)
- Driver cancellation or order modification flows
- Accessibility or mobile responsiveness
- Cross-browser compatibility (Firefox, Edge, Safari)
- API-level or back-end validation

---

## Test Environment

| Component        | Details                          |
|------------------|----------------------------------|
| OS               | Windows 11 Pro (10.0.26200)      |
| IDE              | PyCharm                          |
| Browser          | Google Chrome 145.0.7632.160     |
| ChromeDriver     | 145.0.7632.117                   |
| Python Version   | 3.14.2                           |
| Selenium Version | 4.25.0                           |
| Test Framework   | pytest 8.3.3                     |
| App Under Test   | Urban Routes (TripleTen sandbox) |

---

## Test Approach

| Approach          | Details                                                               |
|-------------------|-----------------------------------------------------------------------|
| Manual Testing    | Not used — fully automated                                            |
| Automated Testing | All 8 test cases automated using Selenium WebDriver                   |
| POM Used          | Yes — Page Object Model implemented in pages.py                       |
| Test Data Files   | Yes — data.py holds all test constants (URL, addresses, phone, card)  |
| Helpers File      | Yes — helpers.py provides retrieve_phone_code() and is_url_reachable()|

### Architecture
- `main.py`    — Test class and all test methods (pytest)
- `pages.py`   — UrbanRoutesPage class with locators and action methods
- `data.py`    — Centralized test data constants
- `helpers.py` — Utility functions (SMS code retrieval, URL reachability)

---

## Test Cases Covered

| #  | Test Case                       | Method                               | Assertion                                    |
|----|---------------------------------|--------------------------------------|----------------------------------------------|
| 1  | Set Routes                      | test_set_routes                      | get_from() and get_to() match input data     |
| 2  | Select Supportive Plan          | test_select_plan                     | Active card .text equals 'Supportive'        |
| 3  | Fill Phone Number               | test_fill_phone_number               | Phone button text matches data.PHONE_NUMBER  |
| 4  | Add Credit Card                 | test_fill_card                       | Payment method text equals 'Card'            |
| 5  | Write Comment for Driver        | test_comment_for_driver              | get_comment() matches data.MESSAGE_FOR_DRIVER|
| 6  | Order Blanket and Handkerchiefs | test_order_blanket_and_handkerchiefs | get_property('checked') ON / OFF / ON        |
| 7  | Order 2 Ice Creams              | test_order_2_ice_creams              | get_ice_cream_count() equals 2               |
| 8  | Order Taxi / Car Search Modal   | test_car_search_model_appears        | modal.is_displayed() returns True            |

---

## Results Summary

| Metric      | Count |
|-------------|-------|
| Total Tests | 8     |
| Passed      | 8     |
| Failed      | 0     |
| Blocked     | 0     |

---

## Defects Found

| # | Bug Description                                                                                             | Severity | Status |
|---|-------------------------------------------------------------------------------------------------------------|----------|--------|
| 1 | Syntax error — stray character '1' on line 104 of main.py prevented test collection                        | High     | Fixed  |
| 2 | Car search modal not appearing — missing driver message prevented the Order button from activating the flow | High     | Fixed  |
| 3 | ChromeDriver version mismatch (v146 installed vs Chrome v145) caused SessionNotCreatedException             | High     | Fixed  |
| 4 | CVV field not registering input via send_keys — required JavaScript native input setter for React onChange  | Medium   | Fixed  |

---

## Known Issues / Limitations

### Flaky Tests
- `test_fill_phone_number` can be sensitive to network latency when retrieving the
  SMS code via `retrieve_phone_code()`. If the server is slow, the log entry may
  not be available in time.

### SMS Dependency
- SMS code retrieval requires performance logging to be enabled in `setup_class` via
  `capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}`.
  If this is removed or misconfigured, `test_fill_phone_number` and
  `test_car_search_model_appears` will fail.

### Timing Issues
- Tests use `time.sleep(2)` pauses between steps for visual verification.
  These are intentional but make the suite slower (~25-90 seconds per test).
  In a CI/CD pipeline these should be replaced with explicit WebDriverWait conditions.

### Environment Issues
- The Urban Routes sandbox server URL in `data.py` is session-specific and expires.
  The URL must be updated each time a new server session is started.
- `webdriver.Chrome()` requires ChromeDriver version to match the installed Chrome
  version exactly. ChromeDriver v145 must be present in `C:\WebDriver\bin\`.

---

## Conclusion

### Overall Status
All 8 automated test cases passed successfully. The full ride-ordering workflow
for the Urban Routes application has been validated end-to-end including address
entry, tariff selection, phone verification, payment setup, driver messaging,
optional items (blanket, ice cream), and taxi ordering with modal confirmation.

### Ready / Not Ready
**READY** — The core ride-order workflow is fully validated. All defects discovered
during development were identified and resolved. The test suite is committed to
both GitHub and GitLab and meets all project requirements defined in Sprint 8.
