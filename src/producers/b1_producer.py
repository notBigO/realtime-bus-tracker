import json
from pykafka import KafkaClient
from datetime import date, datetime
import uuid
import time

# Read coordinates from geojson
input_file = open("../data/b1_coords.json")
json_array = json.load(input_file)
coords = json_array["features"][0]["geometry"]["coordinates"]

client = KafkaClient(hosts="localhost:9092")
topic = client.topics["busCoordData"]


producer = topic.get_sync_producer()  # type: ignore


# Message construct and publish to broker
data = {}
data["busline"] = "0001"


def generate_checkpoint(coords):
    i = 0

    while i < len(coords):
        data["key"] = data["busline"] + "_" + str(uuid.uuid4())
        data["timestamp"] = str(datetime.now())
        data["latitude"] = coords[i][1]
        data["longitude"] = coords[i][0]

        message = json.dumps(data)
        producer.produce(message.encode("ascii"))
        time.sleep(1)

        if i == len(coords) - 1:
            i = 0
        else:
            i += 1


generate_checkpoint(coords)
