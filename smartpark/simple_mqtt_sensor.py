""""Demonstrates a simple implementation of an 'event' listener that triggers
a publication via mqtt"""
from sense_emu import SenseHat
import mqtt_device
import config_parser
from datetime import datetime


class Sensor(mqtt_device.MqttDevice):
    def __init__(self, config):
        # Initialise the Sensor class with MQTT super class configuration
        super().__init__(config)
        self.client.loop_start()
        # Create an instance for SenseHat object
        self.sense_hat = SenseHat()
        print("Sensor: MQTT Connection: ", self.client.is_connected())

    @property
    def read_temperature(self):
        """Returns the temperature from Sense Hat"""
        temperature = self.sense_hat.get_temperature()
        return temperature

    def on_detection(self, message):
        """Triggered when a detection occurs"""
        temperature = self.read_temperature
        self.client.publish('temperature', str(temperature))
        self.client.publish('sensor', message)
        print("Sensor: publishing sensor event: ", message)
        print("MQTT messages published")

    def start_sensing(self):
        """ A blocking event loop that waits for detection events, in this
        case Enter presses"""
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
    config1 = config_parser.parse_config('config.json')
    # Create an instance for the Sensor class
    sensor1 = Sensor(config1)
    print("Sensor initialized")
    # Start the sensing loop
    sensor1.start_sensing()


