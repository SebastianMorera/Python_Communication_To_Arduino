import pytest
import serial

from ArduinoController import ArduinoController
from unittest.mock import patch, MagicMock

@pytest.fixture
def controller():
    yield ArduinoController("TestDevice", "New board", "I2C", 9600, "/dev/ttyUSB0")

@pytest.mark.ArduinoController
def test_arduino_controller_initialization(controller):
    assert controller.device_name == "TestDevice"
    assert controller.board_type == "New board"
    assert controller.protocol == "I2C"
    assert controller.baudrate == 9600
    assert controller.port == "/dev/ttyUSB0"
    assert controller.timeout == 1
    assert not controller.connected
    assert controller.serial_connection is None

@pytest.mark.parametrize(
    "mock_side_effect, expected_connect, expected_connected",
    [
        (None, True, True),  # Successful connection
        (serial.SerialException("Test error"), False, False),  # Failed connection
    ]
)

@patch('ArduinoController.serial.Serial')
@pytest.mark.ArduinoController
def test_arduino_controller_connect(mock_serial, mock_side_effect, expected_connect, expected_connected, controller):
    mock_serial_instance = MagicMock()
    mock_serial.return_value = mock_serial_instance
    mock_serial.side_effect = mock_side_effect

    assert controller.connect() == expected_connect
    assert controller.connected == expected_connected

    if expected_connect:
        mock_serial.assert_called_with(port="/dev/ttyUSB0", baudrate=9600, timeout=1)

@patch('ArduinoController.serial.Serial')
@pytest.mark.ArduinoController
def test_arduino_controller_disconnect(mock_serial, controller):
    mock_serial_instance = MagicMock()
    mock_serial.return_value = mock_serial_instance

    controller.connect()
    controller.disconnect()

    assert controller.connected is False
    mock_serial_instance.close.assert_called_once()

@pytest.mark.parametrize(
    "led_command, is_connected, mock_side_effect, expected_print",
    [
        (b'O', True, None, None),
        (b'O', False, None, "Error: Not connected to TestDevice"),
        (b'O', True, serial.SerialException("Write error"), "Error: Failed to write to serial port: Write error"),
    ]
)
@patch('ArduinoController.serial.Serial')
@pytest.mark.ArduinoController
def test_arduino_controller_turn_on_led(mock_serial, led_command, is_connected, mock_side_effect, expected_print, controller, capsys):
    mock_serial_instance = MagicMock()
    mock_serial.return_value = mock_serial_instance
    mock_serial_instance.write.side_effect = mock_side_effect

    if is_connected:
        controller.connect()

    controller.turn_on_led()

    if is_connected and mock_side_effect is None:
        mock_serial_instance.write.assert_called_once_with(led_command)
    elif expected_print:
        captured = capsys.readouterr()
        assert expected_print in captured.out

@pytest.mark.parametrize(
    "led_command, is_connected, mock_side_effect, expected_print",
    [
        (b'F', True, None, None),
        (b'F', False, None, "Error: Not connected to TestDevice"),
        (b'F', True, serial.SerialException("Write error"), "Error: Failed to write to serial port: Write error"),
    ]
)
@patch('ArduinoController.serial.Serial')
@pytest.mark.ArduinoController
def test_arduino_controller_turn_off_led(mock_serial, led_command, is_connected, mock_side_effect, expected_print, controller, capsys):
    mock_serial_instance = MagicMock()
    mock_serial.return_value = mock_serial_instance
    mock_serial_instance.write.side_effect = mock_side_effect

    if is_connected:
        controller.connect()

    controller.turn_off_led()

    if is_connected and mock_side_effect is None:
        mock_serial_instance.write.assert_called_once_with(led_command)
    elif expected_print:
        captured = capsys.readouterr()
        assert expected_print in captured.out