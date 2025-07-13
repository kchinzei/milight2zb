#!/usr/bin/env python3
#    The MIT License (MIT)
#    Copyright (c) Kiyo Chinzei (kchinzei@gmail.com)
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.

REQUIRED_PYTHON_VERSION = (3, 9)
import paho.mqtt.client as mqtt
import json
import argparse
import sys

defaultHost = '192.168.0.201'
defaultPort = 1883

kTopicsDictList = [
    {'topic_sub': 'milight/01_RGBCWW/', 'type': 'rgbww', 'topic_pub': 'zigbee2mqtt/RGBWW'},
    {'topic_sub': 'milight/02_CWW1/', 'type': 'ww', 'topic_pub': 'zigbee2mqtt/WW_U'},
    {'topic_sub': 'milight/03_CWW2/', 'type': 'ww', 'topic_pub': 'zigbee2mqtt/WW_L'},
    {'topic_sub': 'milight/04_Bedlight/', 'type': 'wled', 'topic_pub': 'wled/1cc53a'}
    ]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for tpDict in kTopicsDictList:
        client.subscribe(tpDict['topic_sub']+'#')
        
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode(encoding='utf-8'))
    
    # which topic we receive?
    for d in kTopicsDictList:
        # if d['topic_sub'] + 'u' == msg.topic and d['type'] == 'wled':
        #    key = next(iter(payload))
        #    val = payload[key]
        #    print(f'{key=} {val=}')
        #    if key in {'status', 'brightness'}:
        #        client.publish(topic=d['topic_pub'], payload=val, qos=1)
        # match payload:
        #    case {'state':state}:
        #        client.publish(topic=d['topic_pub'], payload=state, qos=1)
        #    case {'brightness':brightness}:
        #        client.publish(topic=d['topic_pub'], payload=brightness, qos=1)
        # if d['topic_sub'] + 's' == msg.topic and d['type'] != 'wled':
        if d['topic_sub'] + 's' == msg.topic:
            pub_msg = ''
            # match payload:
            #   case {"bulb_mode":"white", "state":state, "brightness":brightness, "color_temp":color_temp, **kw}:
            #       pub_msg = f'{{"state":"{state}", "color_mode":"color_temp", "brightness":{brightness}, "color_temp":{color_temp}}}'
            #   case {"bulb_mode":"color", "state":state, "brightness":brightness, "color":color, **kw} if d['type'] == 'rgbww':
            #       pub_msg = f'{{"state":"{state}", "brightness":{brightness}, "color":{{"r":{color["r"]}, "g":{color["g"]}, "b":{color["b"]} }} }}'
            if d['type'] == 'wled':
                state = payload["state"]
                brightness = payload["brightness"]
                print(f'{state=} {brightness=}')
                if state == 'OFF':
                    brightness = 0
                client.publish(topic=d['topic_pub'], payload=state, qos=1)
                client.publish(topic=d['topic_pub'], payload=brightness, qos=1)
            elif payload["bulb_mode"] == "white":
                state = payload["state"]
                brightness = payload["brightness"]
                color_temp = payload["color_temp"]
                pub_msg = f'{{"state":"{state}", "color_mode":"color_temp", "brightness":{brightness}, "color_temp":{color_temp}}}'
            elif payload["bulb_mode"] == "color" and d['type'] == 'rgbww':
                state = payload["state"]
                brightness = payload["brightness"]
                color = payload["color"]
                pub_msg = f'{{"state":"{state}", "brightness":{brightness}, "color":{{"r":{color["r"]}, "g":{color["g"]}, "b":{color["b"]} }} }}'
            if pub_msg != '':
                client.publish(topic=d['topic_pub'], payload=pub_msg, qos=1)

def milight2zigbee(host, port, username, password):
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.username_pw_set(username=username, password=password)
    mqttc.connect(host=host, port=port, keepalive=60)

    # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
    mqttc.loop_forever()

def main(argv=None):
    if sys.version_info < REQUIRED_PYTHON_VERSION:
        print(f'Requires python {REQUIRED_PYTHON_VERSION} or newer.', file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(description='Translate MiLight MQTT to Zigbee MQTT')

    required_parser = parser.add_argument_group('required arguments')
    required_parser.add_argument('-u', '--username', metavar='user', type=str, required=True, help=f'username for MQTT host to publish')
    required_parser.add_argument('-p', '--password', metavar='pwd', type=str, required=True, help=f'password for MQTT user')
    parser.add_argument('-H', '--host', metavar='host', type=str, default=defaultHost, help=f'MQTT host (default: {defaultHost})')
    parser.add_argument('-P', '--port', metavar='port', type=int, default=defaultPort, help=f'MQTT port (default: {defaultPort})')
    
    args = parser.parse_args(args=argv)
    milight2zigbee(**vars(args))
    return 0

if __name__ == '__main__':
    sys.exit(main())
