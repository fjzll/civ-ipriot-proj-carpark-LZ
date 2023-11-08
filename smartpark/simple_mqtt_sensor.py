""""Demonstrates a simple implementation of an 'event' listener that triggers
a publication via mqtt"""
from sense_emu import SenseHat
import mqtt_device
import json


class Sensor(mqtt_device.MqttDevice):
    def __init__(self, config):
        # Initialise the Sensor class with MQTT super class configuration
        super().__init__(config)
        # Create an instance for SenseHat object
        self.sense_hat = SenseHat()

    @property
    def read_temperature(self):
        """Returns the temperature from Sense Hat"""
        temperature = self.sense_hat.get_temperature()
        return temperature

    def on_detection(self, message):
        """Triggered when a detection occurs"""
        self.client.publish('sensor', message)

    def start_sensing(self):
        """ A blocking event loop that waits for detection events, in this
        case Enter presses"""
        while True:
            print("Press E when 🚗 entered!")
            print("Press X when 🚖 exited!")
            detection = input("E or X> ").upper()
            if detection == 'E':
                temperature = self.read_temperature
                self.on_detection(f"entered, {temperature}")
            else:
                temperature = self.read_temperature
                self.on_detection(f"exited, {temperature}")


if __name__ == '__main__':
    # Read previous config from file instead of embedding
    file_name = open('config.json', 'r')
    config1 = json.load(file_name)
    # create an instance for the Sensor class
    sensor1 = Sensor(config1)
    print("Sensor initialized")
    # Start the sensing loop
    sensor1.start_sensing()


