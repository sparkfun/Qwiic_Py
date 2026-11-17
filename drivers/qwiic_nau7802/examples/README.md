# Sparkfun NAU7802 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_nau7802_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Nau7802 Ex1 Basic Readings
Demonstrates how to get basic data from the Qwiic Scale.

The key methods showcased by this example are:
- [get_reading()](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#a00162b452ba30d42f9f4befe5412a7c8)
- [available()](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#ab38681e752e91082c926b38d6794b172)

## Qwiic Nau7802 Ex2 Complete Scale
Demonstrates how to calibrate the Qwiic Scale to measure weight

The key methods showcased by this example are:
- [calculate_zero_offset](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#ac390dc8a58df3bea2406c6024e407296)
- [calculate_calibration_factor](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#a9c056fd29c9b76b7d445544dc88c2192)
- [set_zero_offset()](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#ad3388ab14781b6151c35b5f14e8256da)
- [set_calibration_factor()](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#ab53d4dc405cefed6c1bd7ec958b88898)
- [get_weight()](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#a686917c13606551229241806c62d4269)

## Qwiic Nau7802 Ex3 Gain Sample Rate
Demonstrates how to set the gain and sample rate of the Qwiic Scale.

The key methods showcased by this example are:
- [set_gain()](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#a81631b780f7581c9cbe3db324987963a)
- [set_sample_rate()](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#abc4fcc9abeb186c4769c3d0827a6bdd3)
- [calibrate_afe()](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#a7ab7f652e7885cce52e0d9f223953120)

## Qwiic Nau7802 Ex4 Low Power
Demonstrates how to set the Qwiic Scale into low power mode.

The key methods showcased by this example are:
- [power_down](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#ad85ea4158e20bcee11e8a62f886f6d4f)
- [power_up](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#a395afd9b34d87ee6efaade71d276420d)
- [millis](https://docs.sparkfun.com/qwiic_nau7802_py/classqwiic__nau7802_1_1_qwiic_n_a_u7802.html#a2975d767a7498d05ad4254efeff09f55)


