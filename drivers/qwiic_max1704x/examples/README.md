# Sparkfun MAX1704X Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_max1704x_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Max1704X Ex1 Basic
This example will print the gauge's voltage and state-of-charge (SOC) readings

The key methods showcased by this example are: 
- [quick_start()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a02031ba7036090a2a30432490bb2b0d0)
- [set_threshold()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a43af5fb10114bfc5b692d67e752f85a6)
- [get_voltage()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a2564cd5d2c893d2afb619de8936a2662)
- [get_soc()](http://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#ae52eef326f12a3b00249d9d0af8a6e6f)
- [get_alert()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a651ed7f502abd5a278241a9da40bc530)

## Qwiic Max1704X Ex4 Kitchen Sink
This example is an "everything-but-the-kitchen-sink" test of the MAX17048.

The key methods showcased by this example are: 
- [reset()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a616a564310b212f11f700fcb6529340b)
- [get_id()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a659666bbd779020269ff894c85ae979f)
- [get_version()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a3f8dcb6d8031bf08ce2a9444571e0990)
- [set_valrt_max_volts()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a848ee089068727a9c2ce298648af46ce)
- [set_valrt_min_volts()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#af3d6f3292854793c5a22453eafc84a1a)
- [enable_soc_alert()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#ac5d46eb6fc8ee18e9c50809179489ccd)
- [get_hibrt_act_thr()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a2fed7253520d6e9d9775b956c890efa1)
- [get_change_rate()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a9ed5624b0e8811ba01e0d52ee0e23669)
- [is_voltage_high()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a8480f4f13199a1c9142b285d49c0609e)
- [is_voltage_low()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a2e85453b7ebdf8e89b92ea916f0630b0)
- [is_low()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#ae2792891971c02ac24ef161b2acf7b73)
- [is_change()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#a8b71f12bd03346d73a9afbe8d9022e94)
- [is_hibernating()](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html#abf5a178e8f5596af221a412dd39dd312)