import unittest
from smartpark.simple_mqtt_display import Display
from smartpark.config_parser import Config
from smartpark.mqtt_device import MqttDevice
from unittest.mock import MagicMock, patch


class TestDisplay(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment
        """
        self.mock_sense_hat = MagicMock()
        config_instance = Config()
        config = config_instance.parse_config('smartpark/config.json')
        with patch('smartpark.simple_mqtt_display.SenseHat', return_value=self.mock_sense_hat):
            self.display = Display(config)

    def test_display(self):
        """
        Test the display method
        """
        # Define test arguments
        args = ("Time: 13:00", "Spaces: 110", "Temperature: 28")
        # Call the display method
        self.display.display(*args)
        # Assert that show_message was called with the expected arguments
        self.mock_sense_hat.show_message.assert_called_once_with('\n'.join(args),
                                                                 scroll_speed=0.1,
                                                                 text_colour=(255, 255, 0),
                                                                 back_colour=(0, 0, 255))


if __name__ == '__main__':
    unittest.main()

