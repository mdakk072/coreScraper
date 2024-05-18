import pytest
import os
from selenium.webdriver.common.by import By
from unittest.mock import patch, MagicMock
from core.baseDriver import BaseDriver

@pytest.fixture
def base_driver():
    driver_path = "geckodriver"  # Replace with your geckodriver path
    driver = BaseDriver(driver_path=driver_path, headless=True)
    driver.init_driver()
    yield driver
    driver.close_driver()

def test_save_page(base_driver, tmp_path):
    # Mock logger
    with patch('core.baseDriver.Utils.get_logger', return_value=MagicMock()) as mock_logger:
        base_driver.logger = mock_logger

        # Navigate to a test page
        base_driver.navigate_to("https://example.com")

        # Define the file path to save the page
        file_path = tmp_path / "saved.html"

        # Save the page source to the file
        base_driver.save_page(file_path)

        # Verify the file was created
        assert os.path.exists(file_path)

        # Verify the file is not empty
        with open(file_path, "r") as f:
            content = f.read()
            assert len(content) > 0

        # Verify logger calls
        mock_logger.debug.assert_called_with("Page source saved to file.")
