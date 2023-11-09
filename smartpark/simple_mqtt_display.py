import json
import mqtt_device
import time
from sense_emu import SenseHat


class Display(mqtt_device.MqttDevice):
    """Displays the number of cars and the temperature"""
    def __init__(self, config):
        super().__init__(config)
        self.client.on_message = self.on_message
        self.client.subscribe('display')
        self.client.loop_forever()
        self.sense_hat = SenseHat()

    def display(self, *args):
        # Clear the SenseHat LED matrix
        self.sense_hat.clear()
        yellow = (255, 255, 0)
        blue = (0, 0, 255)
        print('*' * 20)
        # Display arguments in SenseHat LED matrix
        for val in args:
            self.sense_hat.show_message(val, text_colour=yellow, back_colour=blue)
            time.sleep(1)
        print('*' * 20)

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()
        # Parse the message and extract free spaces, temperature, time
        current_time = data.split('TIME: ')[1].split(', ')[0]
        spaces = data.split('SPACES: ')[1].split(', ')[0]
        temperature = data.split('TEMPERATURE: ')[1].split(', ')[0]
        # Display the extracted values on Sense Hat emulator
        self.display(f"Time: {current_time}", f"Free spaces: {spaces}", f"Temperature: {temperature}°C")


if __name__ == '__main__':
    # Read config from config.json file
    file_name = open('config.json', 'r')
    config = json.load(file_name)
    # Create an instance of Display class
    display = Display(config)
    file_name.close()

