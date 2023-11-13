import unittest
from smartpark.simple_mqtt_carpark import CarPark
from smartpark.config_parser import parse_config


class TestCarPark(unittest.TestCase):
    def test_available_spaces_within_capacity(self):
        """
        Test the available_spaces is calculated correctly when
        the number of cars is less than the total spaces.
        """
        # Read the configuration from config.json
        config = parse_config("config.json")
        # Create an CarPark instance
        car_park1 = CarPark(config)
        car_park1.total_cars = 25
        car_park1.available_spaces()
        expected_available_spaces = max(0, car_park1.total_spaces - car_park1.total_cars)
        # Assert that the actual and expect available spaces match
        self.assertEqual(car_park1.available_spaces, expected_available_spaces)

    def test_available_spaces_exceed_capacity(self):
        """
        Test the available_spaces will return 0 when
        the number of cars is exceeding the total spaces.
        """
        # Read the configuration from config.json
        config = parse_config("config.json")
        # Create an CarPark instance
        car_park2 = CarPark(config)
        car_park2.total_cars = 130
        car_park2.on_car_entry()
        expected_available_spaces = 0
        # Assert that the actual and expect available spaces match
        self.assertEqual(car_park2.available_spaces, expected_available_spaces)


if __name__ == '__main__':
    unittest.main()

