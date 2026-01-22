import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from conftest import attach_text


@allure.feature("Dropdown")
@allure.story("Select value from dropdown")
@allure.severity(allure.severity_level.CRITICAL)
def test_dropdown_selection(driver, test_logger):
    with allure.step("Open main page"):
        test_logger.info("STEP: Open main page")
        driver.get("https://the-internet.herokuapp.com")

    with allure.step("Open Dropdown page"):
        test_logger.info("STEP: Click 'Dropdown' link")
        driver.find_element(By.LINK_TEXT, "Dropdown").click()

    expected = "Option 2"
    with allure.step("Wait for dropdown (Explicit Wait) and select Option 2"):
        test_logger.info("STEP: Explicit wait for dropdown and select Option 2")
        wait = WebDriverWait(driver, 10)
        dropdown = wait.until(EC.presence_of_element_located((By.ID, "dropdown")))
        select = Select(dropdown)
        select.select_by_visible_text(expected)

    actual = select.first_selected_option.text
    with allure.step("Verify selected value (Expected vs Actual)"):
        test_logger.info(f"ASSERT: Expected={expected}, Actual={actual}")
        attach_text("Expected", expected)
        attach_text("Actual", actual)
        assert actual == expected


@allure.feature("Hover")
@allure.story("Hover over image")
@allure.severity(allure.severity_level.NORMAL)
def test_hover_action(driver, test_logger):
    with allure.step("Open hovers page"):
        test_logger.info("STEP: Open hovers page")
        driver.get("https://the-internet.herokuapp.com/hovers")

    with allure.step("Hover over first image (ActionChains)"):
        test_logger.info("STEP: Hover over first image (ActionChains)")
        figures = driver.find_elements(By.CLASS_NAME, "figure")
        ActionChains(driver).move_to_element(figures[0]).perform()

    expected = True
    with allure.step("Verify caption is visible (Expected vs Actual)"):
        caption = figures[0].find_element(By.CLASS_NAME, "figcaption")
        actual = caption.is_displayed()
        test_logger.info(f"ASSERT: Expected caption visible={expected}, Actual={actual}")
        attach_text("Expected", str(expected))
        attach_text("Actual", str(actual))
        assert actual is True


@allure.feature("Dynamic Controls")
@allure.story("Enable input field")
@allure.severity(allure.severity_level.CRITICAL)
def test_fluent_wait_input_enable(driver, test_logger):
    with allure.step("Open dynamic controls page"):
        test_logger.info("STEP: Open dynamic controls page")
        driver.get("https://the-internet.herokuapp.com/dynamic_controls")

    with allure.step("Click Enable button"):
        test_logger.info("STEP: Click 'Enable' button")
        driver.find_element(By.XPATH, "//button[text()='Enable']").click()

    with allure.step("Wait until input is clickable (Fluent Wait)"):
        test_logger.info("STEP: Fluent wait for input clickable (timeout=15, poll=0.5)")
        fluent_wait = WebDriverWait(driver, timeout=15, poll_frequency=0.5)
        input_field = fluent_wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']"))
        )

    with allure.step("Type text into input"):
        test_logger.info("STEP: Type text into input")
        input_field.send_keys("Fluent wait works!")

    expected = True
    actual = input_field.is_enabled()
    with allure.step("Verify input is enabled (Expected vs Actual)"):
        test_logger.info(f"ASSERT: Expected input enabled={expected}, Actual={actual}")
        attach_text("Expected", str(expected))
        attach_text("Actual", str(actual))
        assert actual is True