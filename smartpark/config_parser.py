"""A class or function to parse the config file and return the values as a dictionary.

The config file itself can be any of the following formats:

- ryo: means 'roll your own' and is a simple text file with key-value pairs separated by an equals sign. For example:
```
location = "Moondalup City Square Parking"
number_of_spaces = 192
```
**you** read the file and parse it into a dictionary.
- json: a json file with key-value pairs. For example:
```json
{location: "Moondalup City Square Parking", number_of_spaces: 192}
```
json is built in to python, so you can use the json module to parse it into a dictionary.
- toml: a toml file with key-value pairs. For example:
```toml
[location]
name = "Moondalup City Square Parking"
spaces = 192
```
toml is part of the standard library in python 3.11, otherwise you need to install tomli to parse it into a dictionary.
```bash
python -m pip install tomli
```
see [realpython.com](https://realpython.com/python-toml/) for more info.

Finally, you can use `yaml` if you prefer.



"""

import json


class Config:
    """Handle the parsing the configuration file: config.json"""

    def __init__(self):
        """Initializes the Config class."""
        self.config = None

    def parse_config(self, config_file_path='config.json'):
        """Parse the config file and return the values as a dictionary"""
        # read and pase the config file from config.json file
        with open(config_file_path, 'r') as config_file:
            self.config = json.load(config_file)
        # return the configuration from config.json file
        return self.config


