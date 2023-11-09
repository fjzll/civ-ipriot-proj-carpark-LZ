from datetime import datetime
import mqtt_device
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage
import config_parser


class CarPark(mqtt_device.MqttDevice):
    """Creates a car park object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config)
        self.total_spaces = config['total-spaces']
        self.total_cars = config['total-cars']
        self.client = paho.Client()
        self.client.on_message = self.on_message
        self.client.subscribe('sensor')
        self.client.subscribe('temperature')
        self.client.loop_forever()
        self._temperature = None

    @property
    def available_spaces(self):
        available = self.total_spaces - self.total_cars
        return max(available, 0)

    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        self._publish_event()
        
    def _publish_event(self):
        readable_time = datetime.now().strftime('%H:%M')
        message = (
            f"TIME: {readable_time}, "
            + f"SPACES: {self.available_spaces}, "
            + "TEMPERATURE: {self.temperature}°C"
        )
        self.client.publish('display', message)

    def on_car_entry(self):
        self.total_cars += 1
        self._publish_event()

    def on_car_exit(self):
        self.total_cars -= 1
        self._publish_event()

    def on_message(self, client, userdata, msg: MQTTMessage):
        payload = msg.payload.decode()
        # self.temperature = ... # Extracted value
        # Extract temperature from payload
        if msg.topic == "temperature":
            self.temperature = float(payload)
        if 'exit' in payload:
            self.on_car_exit()
        else:
            self.on_car_entry()


if __name__ == '__main__':
    # Read config from json file  Lili Zheng
    config = config_parser.parse_config('config.json')
    car_park = CarPark(config)
    print("Car park initialized")


