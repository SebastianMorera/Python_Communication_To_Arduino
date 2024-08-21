import serial

class ArduinoController:
    def __init__(self, device_name: str, protocol: str, baudrate: int, port: str, board_type= "Uno", timeout=1):
        self.device_name = device_name
        self.board_type = board_type
        self.protocol = protocol
        self.baudrate = baudrate
        self.port = port
        self.timeout = timeout
        self.connected = False
        self.serial_connection = None

    def connect(self) -> bool:
        try:
            self.serial_connection = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            self.connected = True
            return True
        except serial.SerialException as e:
            self.connected = False
            print(f"Error: Connection could not be established. Error: {str(e)}")
            return False

    def disconnect(self) -> None:
        if self.connected:
            self.serial_connection.close()
            self.connected = False
            print(f"Connection successfully closed with {self.device_name}")

    def turn_on_led(self) -> None:
        if not self.connected:
            print(f"Error: Not connected to {self.device_name}")

        try:
            self.serial_connection.write(b'O')
        except serial.SerialException as e:
            print(f"Error: Failed to write to serial port: {str(e)}")

    def turn_off_lef(self) -> None:
        if not self.connected:
            print(f"Error: Not connected to {self.device_name}")

        try:
            self.serial_connection.write(b'F')
        except serial.SerialException as e:
            print(f"Error: Failed to write to serial port: {str(e)}")