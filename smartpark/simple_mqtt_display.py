import mqtt_device
import time
from sense_emu import SenseHat
from config_parser import Config


class Display(mqtt_device.MqttDevice):
    """Represents a display object to show information on SenseHat Emulator"""
    def __init__(self, config):
        """Initializes the display class with MQTT super class configuration"""
        super().__init__(config)
        self.client.on_message = self.on_message
        self.client.subscribe('display')
        self.sense_hat = SenseHat()

        if __name__ == '__main__':
            self.client.loop_forever()
            # print("Display: MQTT connection: ", self.client.is_connected())

    def display(self, *args):
        """Displays the arguments on the SenseHat emulator"""
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
        """Callback to handle MQTT display messages"""
        data = msg.payload.decode()
        # print("Display: MQTT message received: ", data)
        # Parse the message and extract free spaces, temperature, time from payload data
        current_time = data.split('TIME: ')[1].split(', ')[0]
        spaces = int(data.split('SPACES: ')[1].split(', ')[0])
        temperature = data.split('TEMPERATURE: ')[1].split(', ')[0]
        # Display the extracted values on Sense Hat emulator
        self.display(f"Time: {current_time}", f"Spaces: {spaces}", f"Temperature: {temperature}")


if __name__ == '__main__':
    # Read config from config.json file by calling the parse_config method
    config = Config()
    config_data = config.parse_config('config.json')
    # Create an instance of Display class
    display = Display(config_data)
    # print("Display initialized")


