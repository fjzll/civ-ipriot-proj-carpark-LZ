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
import os.path


class Config:

    def __init__(self):
        self.config = None

    def parse_config(self, config_file_path='config.json'):
        # read and pase the config file from config.json file
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
        """Parse the config file and return the values as a dictionary"""
        # return the configuration from config.json file
        return config_data

    def write_config(self, config_file_parth='config.json'):
        # Write the updated configuration data to config.json
        with open(config_file_path, 'w') as config_file:
            json.dump(self.config, config_file)



