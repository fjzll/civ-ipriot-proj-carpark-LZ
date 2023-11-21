""""Demonstrates a simple implementation of an 'event' listener that triggers
a publication via mqtt"""
from sense_emu import SenseHat
import mqtt_device
from config_parser import Config
from datetime import datetime


class Sensor(mqtt_device.MqttDevice):
    """
    Represents a sensor that listens for events and publishes events via MQTT
    """
    def __init__(self, config):
        """
        Initialise the Sensor class with MQTT super class configuration.
        """
        super().__init__(config)
        self.client.loop_start()
        # Create an instance for SenseHat object
        self.sense_hat = SenseHat()
        print("Sensor: MQTT Connection: ", self.client.is_connected())

        if __name__ == '__main':
            self.start_sensing()

    @property
    def read_temperature(self):
        """Returns the temperature from Sense Hat"""
        temperature = self.sense_hat.get_temperature()
        return temperature

    def on_detection(self, message):
        """Triggered when a detection occurs"""
        # print("Detection Message:", message)
        temperature = self.read_temperature
        self.client.publish('temperature', temperature)
        # print("Sensor: publishing sensor event: ", message)
        self.client.publish('sensor', message)
        # print("MQTT messages published")

    def start_sensing(self):
        """ A blocking event loop that waits for detection events.
        The function prompts users inputs to represent sensing car
        entering and exiting. Input 'E' for car entry and 'X' for
        car exit. It then publishes messages by calling on_detection
        method.
        """
        while True:
            print("Press E when car entered!")
            print("Press X when car exited!")
            detection = input("E or X> ").upper()
            readable_time = datetime.now().strftime('%H:%M')
            temperature = self.read_temperature
            if detection == 'E':
                self.on_detection(f"entered, {temperature}, {readable_time}")
            else:
                self.on_detection(f"exited, {temperature}, {readable_time}")


if __name__ == '__main__':
    # Read previous config from file instead of embedding
    config = Config()
    config_data = config.parse_config('config.json')
    # Create an instance for the Sensor class
    sensor1 = Sensor(config_data)
    print("Sensor initialized")
    # Start the sensing loop
    sensor1.start_sensing()


