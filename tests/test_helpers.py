import pytest
from unittest.mock import MagicMock

# Import the function to test
from functions.helpers import power_on


# Mocking GPIO module
@pytest.fixture
def mock_gpio():
    import sys

    sys.modules["RPi"] = MagicMock()
    sys.modules["RPi.GPIO"] = MagicMock()
    import RPi.GPIO as GPIO

    return GPIO


# Test for turning on power
def test_power_on(mock_gpio):
    RELAY_CHANNEL = 4
    ON = True
    result = power_on(RELAY_CHANNEL, ON)
    mock_gpio.setup.assert_called_once_with(RELAY_CHANNEL, mock_gpio.OUT)
    mock_gpio.output.assert_called_once_with(RELAY_CHANNEL, mock_gpio.HIGH)
    assert result == 1


# Test for turning off power
def test_power_off(mock_gpio):
    RELAY_CHANNEL = 4
    ON = False
    result = power_on(RELAY_CHANNEL, ON)
    mock_gpio.setup.assert_called_once_with(RELAY_CHANNEL, mock_gpio.OUT)
    mock_gpio.output.assert_called_once_with(RELAY_CHANNEL, mock_gpio.LOW)
    assert result == 0


# Test for invalid input type
def test_invalid_input(mock_gpio):
    RELAY_CHANNEL = 4
    ON = "invalid"
    with pytest.raises(TypeError):
        power_on(RELAY_CHANNEL, ON)
    mock_gpio.setup.assert_not_called()
    mock_gpio.output.assert_not_called()
