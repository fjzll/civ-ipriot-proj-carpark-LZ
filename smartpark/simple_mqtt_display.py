import mqtt_device
import time
from sense_emu import SenseHat
import config_parser


class Display(mqtt_device.MqttDevice):
    """Displays the number of cars and the temperature"""
    def __init__(self, config):
        super().__init__(config)
        self.client.on_message = self.on_message
        self.client.subscribe('display')
        self.client.loop_start()
        self.sense_hat = SenseHat()
        print("Display: MQTT connection: ", self.client.is_connected())

    def display(self, *args):
        # Clear the SenseHat LED matrix
        self.sense_hat.clear()
        yellow = (255, 255, 0)
        blue = (0, 0, 255)
        print('*' * 20)
        # Display arguments in SenseHat LED matrix
        for val in args:
            self.sense_hat.show_message(val, scroll_speed=0.1, text_colour=yellow, back_colour=blue)
            time.sleep(1)
            print(f"Display Class received: {val}")
        print('*' * 20)

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()
        print("Display: MQTT message received: ", data)
        # Parse the message and extract free spaces, temperature, time
        current_time = data.split('TIME: ')[1].split(', ')[0]
        spaces = int(data.split('SPACES: ')[1].split(', ')[0])
        temperature = float(data.split('TEMPERATURE: ')[1].split(', ')[0])
        # Display the extracted values on Sense Hat emulator
        self.display(f"Time: {current_time}", f"Spaces: {spaces}", f"Temperature: {temperature}°C")


if __name__ == '__main__':
    # Read config from config.json file by calling the parse_config method
    config = config_parser.parse_config('config.json')
    # Create an instance of Display class
    display = Display(config)
    print("Display initialized")


