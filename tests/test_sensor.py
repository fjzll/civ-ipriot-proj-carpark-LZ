import unittest
from smartpark.simple_mqtt_sensor import Sensor
from unittest.mock import MagicMock
from smartpark.config_parser import parse_config


class TestSensor(unittest.TestCase):
    def test_read_temperature(self):
        """
        Test the read_temperature method
        """
        # Mock the senseHat
        mock_sense_hat = MagicMock()
        # Read the configuration from config.json
        config = parse_config('config.json')
        sensor = Sensor(config)
        # Set the return value for get_temperature
        mock_sense_hat.get_temperature.return_value = 25.0
        temperature = sensor.read_temperature()
        self.assertEqual(temperature, 25.0)


if __name__ == '__main__':
    unittest.main()

