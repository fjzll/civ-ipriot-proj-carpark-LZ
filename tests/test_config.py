import unittest

import json  # you can use toml, json,yaml, or ryo for your config file

import smartpark.config_parser as pc


class TestConfigParsing(unittest.TestCase):
    def test_parse_config_has_correct_location_and_spaces(self):
        # read from a configuration file
        with open('config.json', 'r') as file:
            config = json.load(file)
            parking_lot = pc.parse_config(config)
            self.assertEqual(parking_lot['location'], "Moondalup City Square Parking")
            self.assertEqual(parking_lot['total_spaces'], 130)


if __name__ == '__main__':
    unittest.main()
