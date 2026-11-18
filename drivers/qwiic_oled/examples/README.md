# Sparkfun OLED Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

Examples 1 to 4 use the Micro OLED by default. To use another display, uncomment the line that creates a `QwiicOLEDDisplay` (0.91in, 128x32) or a `QwiicLargeOLED` (1.3in, 128x64) at the top of the example.

## Example 1: Splash Screen
`qwiic_oled_ex1_splash_screen.py`

Simple Example for an OLED Display that displays the SparkFun splash screen.

The key methods showcased by this example are: 

- `clear()`
- `display()`
- `get_screenbuffer()`
- `oled_logos.add_logo()`

## Example 2: Hello World
`qwiic_oled_ex2_hello_world.py`

Example for writing "Hello World" to an OLED Display.

The key methods showcased by this example are: 

- `print()`

## Example 3: Demo
`qwiic_oled_ex3_demo.py`

A full-featured example showing various features of the display driver for Qwiic OLED displays.

The key methods showcased by this example are: 

- `get_lcd_width()`
- `get_lcd_height()`
- `line()`
- `rect()`
- `rect_fill()`
- `circle()`
- `set_font_type()`
- `set_cursor()`

## Example 4: Cube
`qwiic_oled_ex4_cube.py`

Rotating cube example for a Qwiic OLED Device.

The key methods showcased by this example are: 

- `line()`

## Example 5: Micro Bitmap
`qwiic_oled_ex5_micro_bitmap.py`

Example for the Qwiic Micro OLED display that displays Bender's face!

The key methods showcased by this example are: 

- `draw_bitmap()`
