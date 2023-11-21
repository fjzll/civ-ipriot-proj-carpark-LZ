import unittest
from smartpark.simple_mqtt_carpark import CarPark
from smartpark.simple_mqtt_sensor import Sensor
from smartpark.simple_mqtt_display import Display
from smartpark.config_parser import Config
from smartpark.mqtt_device import MqttDevice


class TestCarPark(unittest.TestCase):
    """Test cases for the CarPark class and related components."""

    def setUp(self):
        """
        Set up the test environment
        """
        # Read configuration from "config.json" and create a CarPark instance for tests
        config_instance = Config()
        self.config = config_instance.parse_config("smartpark/config.json")
        self.car_park = CarPark(self.config)

    def test_car_park_is_instantiated(self):
        """
        Test if a CarPark instance is instantiated
        """
        self.assertIsInstance(self.car_park, CarPark)

    def test_sensor_is_instantiated(self):
        """
        Test if a Sensor instance is instantiated correctly
        """
        self.assertIsInstance(Sensor(self.config), Sensor)

    def test_display_is_instantiated(self):
        """
        Test if a Display instance is instantiated correctly
        """
        self.assertIsInstance(Display(self.config), Display)

    def test_available_spaces_within_capacity(self):
        """
        Test the available_spaces is calculated correctly when
        the number of cars is less than the total spaces.
        """
        self.car_park.total_cars = 25
        expected_available_spaces = max(0, self.car_park.total_spaces - self.car_park.total_cars)
        # Assert that the actual and expect available spaces match
        self.assertEqual(self.car_park.available_spaces, expected_available_spaces)

    def test_available_spaces_exceed_capacity(self):
        """
        Test the available_spaces will return 0 when
        the number of cars is exceeding the total spaces.
        """
        self.car_park.total_cars = 130
        self.car_park.on_car_entry()
        expected_available_spaces = 0
        # Assert that when more cars enter the car park when it is full, the available spaces
        # will not be negative
        self.assertEqual(self.car_park.available_spaces, expected_available_spaces)


if __name__ == '__main__':
    unittest.main()
