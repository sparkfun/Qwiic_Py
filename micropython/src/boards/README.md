# boards files
the ```board``` files are used to configure the ```${BOARDNAME}``` for rshell as well as driver-specific definitions.

for example the **micropython_rp2040_i2c** driver requires values for *qwii_id*, *qwiic_scl*, and *qwiic_sda*.

``` python
from machine import Pin
name='rp2040_promicro'    # provides the name used in rshell
qwiic_id=0                # indicates which i2c peripheral to use
qwiic_scl=Pin(17)         # which pin for scl
qwiic_sda=Pin(16)         # which pin for sda
```