# python-mobilealerts

[![Python Version](https://img.shields.io/pypi/pyversions/mobilealerts.svg)](https://pypi.org/project/mobilealerts/) [![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/PlusPlus-ua/python-mobilealerts/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit) [![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/PlusPlus-ua/python-mobilealerts/blob/master/.pre-commit-config.yaml) [![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/PlusPlus-ua/python-mobilealerts/releases) [![License](https://img.shields.io/github/license/PlusPlus-ua/python-mobilealerts)](https://github.com/PlusPlus-ua/python-mobilealerts/blob/master/LICENSE)



## About this fork

This is [Johnnyyr/python-mobilealerts](https://github.com/Johnnyyr/python-mobilealerts),
a fork of [PlusPlus-ua/python-mobilealerts](https://github.com/PlusPlus-ua/python-mobilealerts).
The original project and authors remain credited below; the MIT license and copyright
notices are retained unchanged. Links and badges referring to PyPI describe the upstream
package, not a release of this fork.

This fork adds optional IPv4 unicast control for gateways on routed networks.
It is used by [Johnnyyr/ha_mobilealerts](https://github.com/Johnnyyr/ha_mobilealerts).
The Python distribution/import name stays `mobilealerts`, so existing imports work.
Changes are maintained separately so they can be proposed upstream.

The upstream Git tree contained older sensor code than the integration's published
`mobilealerts==0.1.13` dependency. `mobilealerts/sensor.py` is synchronized with the
[0.1.13 PyPI distribution](https://pypi.org/project/mobilealerts/0.1.13/), preserving
measurement restoration, previous rain totals and unknown pre-reception values.
The tests cover these API differences. Fork version: `0.1.14.dev0`.

## Gateways on another subnet

```python
from mobilealerts import Gateway

# Probe exactly one IPv4 address; no routed broadcast/relay is required.
gateways = await Gateway.discover(gateway_ip="192.0.2.81")
# Persist both MAC identity and configured target address in your application.
gateway = Gateway("001D8C0DF7E1", gateway_ip="192.0.2.81")
if not await gateway.init():
    raise RuntimeError("Gateway did not return a valid configuration")
```

`gateway_ip` is an optional final argument to `Gateway` and `Gateway.discover`;
existing positional arguments retain their meaning. Omitting it keeps broadcast
behavior. Providing it makes discovery, configuration writes, refresh, ping,
proxy attach/detach and reboot use the same unicast destination on UDP 8003.
Invalid, multicast, unspecified and limited-broadcast targets are rejected.
Socket receive deadlines are handled by asyncio, so sockets remain nonblocking.

A fixed proxy listener already works with `Proxy(handler, local_ip, local_port)`.
Permit UDP 8003 from the controller to the gateway, plus the selected proxy TCP
port from the gateway to the controller, with stateful replies. Reserve the gateway
IP through DHCP. No public Internet port forwarding is needed.

For the companion HA fork, Home Assistant installs an immutable source archive
of this fork automatically. Installing `mobilealerts` from PyPI alone does not
install this unicast extension. For local development:

```bash
python -m pip install -e . pytest
TZ=UTC python -m pytest -q tests
```

## Python classes for MobileAlerts gateway and sensors

Library act as proxy server which intercepts all measurements and sensors properties which sends MobileAlerts gateway to the cloud. 

Everything works in asynchronous way in order to build on the base of this library [Home assistant](https://github.com/home-assistant/core) integration.

## Installation

```bash
pip install -U mobilealerts
```

or install with `Poetry`

```bash
poetry add mobilealerts
```

## 🛡 License

[![License](https://img.shields.io/github/license/PlusPlus-ua/python-mobilealerts)](https://github.com/PlusPlus-ua/python-mobilealerts/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/PlusPlus-ua/python-mobilealerts/blob/master/LICENSE) for more details.

## Credits

This project was inspired and developed on the base of [MMMMobileAlerts](https://github.com/sarnau/MMMMobileAlerts)

This project was generated with [python-package-template](https://github.com/TezRomacH/python-package-template)
