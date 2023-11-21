import unittest
import json  # you can use toml, json,yaml, or ryo for your config file
from smartpark.config_parser import Config


class TestConfigParsing(unittest.TestCase):
    """Test case for the Config class"""
    def test_parse_config_has_correct_location_and_spaces(self):
        # read from a configuration file
        with open('smartpark/config.json', 'r') as file:
            config_data = json.load(file)
        config = Config()
        parking_lot = config.parse_config()

        expected_location = "Moondalup"
        expected_spaces = 130

        self.assertEqual(expected_location, parking_lot['CarParks'][0]['location'])
        self.assertEqual(expected_spaces, parking_lot['CarParks'][0]['total-spaces'])


if __name__ == '__main__':
    unittest.main()
