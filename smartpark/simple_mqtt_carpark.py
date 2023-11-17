from datetime import datetime
import mqtt_device
import paho.mqtt.client as paho
import config_parser
from sense_emu import SenseHat


class CarPark(mqtt_device.MqttDevice):
    """Creates a car park object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config)
        self.total_spaces = config["CarParks"][0]['total-spaces']
        self.total_cars = config["CarParks"][0]['total-cars']
        self.client.on_message = self.on_message
        self.client.subscribe('sensor')
        # self.client.subscribe('temperature')
        self.sense_hat = SenseHat()
        self._temperature = None
        self.client.loop_forever()
        # print("CarPark: MQTT Connection: ", self.client.is_connected())

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
            + f"TEMPERATURE: {self.temperature}°C"
        )
        print(f"Display: publishing display event: {message}")
        self.client.publish('display', message)

    def on_car_entry(self):
        self.total_cars += 1
        self._publish_event()

    def on_car_exit(self):
        self.total_cars -= 1
        self._publish_event()

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"CarPark: Received MQTT message: {payload}")
        # Extract the temperature value from payload
        parts = payload.split(',')
        temperature = float(parts[1])
        # if msg.topic == 'temperature':
            # self.temperature = float(payload)
        # if msg.topic == 'sensor':
        if 'exited' in payload:
            self.on_car_exit()
            # print("exit")
        else:
            self.on_car_entry()
            # print("enter")


if __name__ == '__main__':
    # Read config using the parse_config function from config_parser module
    config = config_parser.parse_config('config.json')
    car_park = CarPark(config)
    # print("Car park initialized")
