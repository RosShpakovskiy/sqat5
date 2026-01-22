import os
import logging
from datetime import datetime

import pytest
import allure

from selenium import webdriver
from selenium.webdriver.edge.options import Options


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

def attach_text(name: str, text: str):
    allure.attach(text, name=name, attachment_type=allure.attachment_type.TEXT)

def attach_file_text(name: str, path: str):
    if os.path.exists(path):
        with open(path, "rb") as f:
            allure.attach(f.read(), name=name, attachment_type=allure.attachment_type.TEXT)

@pytest.fixture(autouse=True)
def test_logger(request):
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    test_name_safe = (
        request.node.name.replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(logs_dir, f"{test_name_safe}_{timestamp}.log")

    logger = logging.getLogger(test_name_safe)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        for h in list(logger.handlers):
            logger.removeHandler(h)

    fh = logging.FileHandler(log_path, encoding="utf-8")
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    request.node._logger = logger
    request.node._log_path = log_path

    logger.info("TEST START")
    logger.info(f"Test: {request.node.nodeid}")

    yield logger

    logger.info("TEST END")

    for h in logger.handlers:
        try:
            h.flush()
        except Exception:
            pass

    attach_file_text("Execution Log", log_path)

    for h in list(logger.handlers):
        try:
            h.close()
        finally:
            logger.removeHandler(h)


@pytest.fixture
def driver(request):
    logger = getattr(request.node, "_logger", None)

    edge_options = Options()
    edge_options.add_argument("--start-maximized")

    drv = webdriver.Edge(options=edge_options)

    drv.implicitly_wait(10)
    if logger:
        logger.info("Browser started: Microsoft Edge")
        logger.info("Implicit wait set: 10 seconds")

    yield drv

    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        if logger:
            logger.error("Test FAILED - capturing screenshot and page source...")

        try:
            allure.attach(
                drv.get_screenshot_as_png(),
                name="Screenshot on failure",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            if logger:
                logger.exception(f"Failed to capture screenshot: {e}")

        try:
            attach_text("Page Source on failure", drv.page_source)
        except Exception as e:
            if logger:
                logger.exception(f"Failed to attach page source: {e}")

    try:
        drv.quit()
        if logger:
            logger.info("Browser closed")
    except Exception as e:
        if logger:
            logger.exception(f"Error while closing browser: {e}")
