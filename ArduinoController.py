import serial

class ArduinoController:
    def __init__(self, device_name, protocol, baudrate, port, board_type= "Uno", timeout=1):
        self.device_name = device_name
        self.board_type = board_type
        self.protocol = protocol
        self.baudrate = baudrate
        self.port = port
        self.timeout = timeout
        self.connected = False
        self.serial_connection = None

    def connect(self):
        try:
            self.serial_connection = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            self.connected = True
            print(f"Connection established with {self.device_name} at port {self.port} and baudrate of {self.baudrate}")
        except serial.SerialException as e:
            self.connected = False
            print(f"Error: Connection could not be established. Error: {str(e)}")

    def disconnect(self):
        if self.connected:
            self.serial_connection.close()
            self.connected = False
            print(f"Connection successfully closed with {self.device_name}")

    def turn_on_led(self):
        if self.connected:
            self.serial_connection.write(b'O')
        else:
            print(f"Error: Not connected to {self.device_name}")

    def turn_off_lef(self):
        if self.connected:
            self.serial_connection.write(b'F')
        else:
            print(f"Error: Not connected to {self.device_name}")
