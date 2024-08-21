from time import perf_counter

from ArduinoController import ArduinoController

def SerialCommunicator():
    arduino = ArduinoController(
        device_name="Arduino",
        protocol="USB",
        baudrate=9600,
        port='/dev/cu.usbmodem14101')

    if arduino.connect():
        print(f"Connection established with {arduino.device_name} at port {arduino.port} and baudrate of {arduino.baudrate}")

        continue_loop = True
        while continue_loop:
            print("Enter 'O' to turn the led on, 'F' to turn the led off, 'Q' to quit")
            user_selection = input().upper()

            match user_selection:
                case 'O':
                    arduino.turn_on_led()
                case 'F':
                    arduino.turn_off_lef()
                case 'Q':
                    continue_loop = False
                case __:
                    print("Wrong selection entered, please try again.")

        arduino.disconnect() if arduino.connected else print(f"{arduino.device_name} was not connected")


if __name__ == "__main__":
    SerialCommunicator()