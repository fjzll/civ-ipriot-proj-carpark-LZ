from datetime import datetime
import mqtt_device
import paho.mqtt.client as paho
from config_parser import Config
from sense_emu import SenseHat
import json


class CarPark(mqtt_device.MqttDevice):
    """
    Represents a car park object to store the state of cars in the lot.
    Manages car entries, exits and calculates available parking spaces.
    Listens to sensor events and publishes to display topic via MQTT.
    Update the available spaces and write it to the configuration file.
    """

    def __init__(self, config):
        """
        Initialize the CarPark class with MQTT super class configuration.
        """
        super().__init__(config)
        self.config = config
        self.total_spaces = config["CarParks"][0]['total-spaces']
        self.total_cars = config["CarParks"][0]['total-cars']
        self.client.on_message = self.on_message
        self.client.subscribe('sensor')
        self.client.subscribe('temperature')
        self.sense_hat = SenseHat()
        self._temperature = None

        if __name__ == '__main__':
            self.client.loop_forever()
            # print("CarPark: MQTT Connection: ", self.client.is_connected())

    @property
    def available_spaces(self):
        """Return the number of available parking spaces."""
        available = self.total_spaces - self.total_cars
        return max(available, 0)

    @property
    def temperature(self):
        """Return the temperature from Sense Hat"""
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        """Set the temperature and publishes the event"""
        self._temperature = value
        self._publish_event()
        
    def _publish_event(self):
        """Publishes the display event with time, available spaces and temperature"""
        readable_time = datetime.now().strftime('%H:%M')
        message = (
            f"TIME: {readable_time}, "
            + f"SPACES: {self.available_spaces}, "
            + f"TEMPERATURE: {self.temperature}°C"
        )
        print(f"Display: publishing display event: {message}")
        self.client.publish('display', message)

    def on_car_entry(self):
        """
        Update the available spaces when a car enters and write it to
        the config.json file.
        Publish the display events when a car enters.
        """
        self.total_cars += 1
        # Update the available spaces in the configuration
        self.config['CarParks'][0]['available-spaces'] = self.available_spaces
        with open('config.json', 'w') as config_file:
            json.dump(self.config, config_file, indent=2)
        self._publish_event()

    def on_car_exit(self):
        """
         Update the available spaces when a car exits and write it to
         the config.json file.
         Publish the display events when a car exits.
         """
        self.total_cars -= 1
        # Update the configuration spaces in the configuration
        self.config['CarParks'][0]['available-spaces'] = self.available_spaces
        with open('config.json', 'w') as config_file:
            json.dump(self.config, config_file, indent=2)
        self._publish_event()

    def on_message(self, client, userdata, msg):
        """Callback to handle MQTT messages"""
        payload = msg.payload.decode()
        # print(f"CarPark: Received MQTT message: {payload}")
        # Extract the temperature value from payload
        if msg.topic == 'temperature':
            self.temperature = float(payload)
            print("CarPark temperature update: ", self.temperature)
        if msg.topic == 'sensor':
            if 'exited' in payload:
                self.on_car_exit()
                # print("exit")
            else:
                self.on_car_entry()
                # print("enter")


if __name__ == '__main__':
    # Read config using the parse_config function from config_parser module
    config = Config()
    config_data = config.parse_config('config.json')
    car_park = CarPark(config_data)
    # print("Car park initialized")
