# milight2zb

Translate MiLight-hub MQTT to Zigbee MQTT.
Support RGB and white with color temperature.

### required arguments
- **-u user, --username user**
  username for MQTT host to publish
- **-p pwd, --password pwd**
  password for MQTT user

### optional arguments:
- **-h, --help**            show this help message and exit
- **-H host, --host host**  MQTT host (default: 192.168.0.201)
- **-P port, --port port**  MQTT port (default: 1883)

## What it is for?

This mini project is to join MiLight remote into MQTT/Zigbee system.

MiLight (Recently renamed to MiBoxer) is a brand for smart bulb and lighting solutions.
Recent drivers do speak Zigbee MQTT.
But remote controllers like [B4](https://miboxer.com/product/4-zone-panel-remote-rgbcct) do not.
Instead they communicate on 2.4 GHz Wifi band using undocumented protocol.

[ESP MiLight hub](https://github.com/sidoh/esp8266_milight_hub/) by sidoh is a MiLight remote/gateway that can listen MiLight protocol and translate to other format including MQTT.
This MQTT is different from that of MiBoxer Zigbee drivers.

`milight2zb` translates MQTT state messages from ESP MiLight hub into MiBoxer Zigbee MQTT so that the other devices can understand it.

<img src="https://miboxer.com/wp-content/uploads/b4-1-300x300.jpg" width="60"> → Wifi  
→ [ESP MiLight hub](https://github.com/sidoh/esp8266_milight_hub/) → (Own MQTT)  
→ `milight2zb` → (Zigbee MiBoxer MQTT)  
→ <img src="https://www.zigbee2mqtt.io/logo.png" width="60">


## Dependency

- Python 3.9 or later
- [paho MQTT client](https://pypi.org/project/paho-mqtt/) `pip3 install paho-mqtt`


## Future to do

- Fork [ESP MiLight hub](https://github.com/sidoh/esp8266_milight_hub/) so that it directly speaks Zibgee MQTT.