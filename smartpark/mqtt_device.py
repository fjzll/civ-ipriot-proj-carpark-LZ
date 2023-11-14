import paho.mqtt.client as paho


class MqttDevice:
    def __init__(self, config):
        self.name = config["CarParks"][0]['name']
        self.location = config["CarParks"][0]['location']
        # Configure broker
        self.broker = config["CarParks"][0]['broker']
        self.port = config["CarParks"][0]['port']

        # Define topic components:
        self.topic_root = config["CarParks"][0]['topic-root']
        self.devices = []
        for sensor_config in config["CarParks"][0]["Sensors"]:
            sensor_name = sensor_config["name"]
            sensor_type = sensor_config["type"]
            sensor_topic_qualifier = sensor_config['topic-qualifier']
            sensor_device = {'name': sensor_name, 'type': sensor_type, 'topic_qualifier': sensor_topic_qualifier}
            self.devices.append(sensor_device)
        for display_config in config["CarParks"][0]["Displays"]:
            display_name = display_config["name"]
            display_topic_qualifier = display_config['topic-qualifier']
            display_device = {'name': display_name, 'topic_qualifier': display_topic_qualifier}
            self.devices.append(display_device)
        self.topic = self._create_topic_string()

        # initialise a paho client and bind it to the object (has-a)
        self.client = paho.Client()
        self.client.connect(self.broker, self.port)

    def _create_topic_string(self):
        topic_string = []
        for device in self.devices:
            topic_string.append(f"{self.topic_root}/{self.location}/{self.name}/"
                                f"{device['name']}/{device['topic_qualifier']}")
        return topic_string
