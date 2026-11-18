# SparkFun Qwiic Python Package

`sparkfun-qwiic` installs every SparkFun [Qwiic](https://www.sparkfun.com/qwiic) Python driver, plus the `qwiic` module that finds connected Qwiic devices and creates their driver objects.

```sh
pip install sparkfun-qwiic
```

```python
import qwiic

print(qwiic.list_devices())                 # [(0x77, 'Qwiic BME280', 'QwiicBME280'), ...]
sensor = qwiic.create_device("QwiicBME280")
sensor.begin()
print(sensor.get_temperature_celsius())
```

| Function | Returns |
| --- | --- |
| `scan()` | Addresses of every device on the bus |
| `list_devices()` | `(address, device name, class name)` for every connected device a driver exists for |
| `list_available_drivers(addresses=None)` | The same, for any addresses, connected or not |
| `get_devices()` | A driver object for every connected device |
| `create_device(device)` | The driver object for one device, by class name, device name, address or `list_devices()` entry |
| `qwiic.QwiicBME280`, ... | Any driver class, imported on first use |

Every function takes an optional `i2c_bus` to choose the bus (see [qwiic_i2c](https://github.com/sparkfun/Qwiic_Py/tree/main/qwiic_i2c)).

On MicroPython and CircuitPython, install only the drivers you need (see the [repository README](https://github.com/sparkfun/Qwiic_Py)); `qwiic` skips drivers that aren't installed.

Source, issues and the full driver list: [github.com/sparkfun/Qwiic_Py](https://github.com/sparkfun/Qwiic_Py).
