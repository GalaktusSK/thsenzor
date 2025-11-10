import collections

# unique device id
DEVICE_ID = 'ab123cd'

# defines the microcontroller's CPU clock frequency (in Hz)
CPU_FREQ = 125 * 1_000_000

# pins configuration
NP_PIN = 18
BTN_PIN = 20
DHT_PIN = 27
I2C_SDA_PIN = 4  # I2C data line (SDA)
I2C_SCL_PIN = 5  # I2C clock line (SCL)
RTC_ALARM_PIN = 6  # GPIO pin for RTC alarm signal

# settings configuration
SETTINGS_FILE = '/settings.json'

# path to the CSV file containing measurement data
MEASUREMENTS_FILE = '/measurements.csv'

# duration for which the button must be held to trigger specific actions
LONG_PRESS_DURATION = 6 * 1000  # for factory reset
SHORT_PRESS_DURATION = 3 * 1000  # for web portal

# SSID of admin WiFi network
SENSOR_SSID = f'thsensor-{DEVICE_ID}'
SENSOR_WIFI_PASSWORD = 'thsensor'


# temperature units
class TempUnit:
    IMPERIAL: str = 'imperial'
    STANDARD: str = 'standard'
    METRIC: str = 'metric'


# class defines basic RGB color constants for the NeoPixel LED.
class Color:
    RED: tuple = (255, 0, 0)
    GREEN: tuple = (0, 255, 0)
    BLUE: tuple = (0, 0, 255)
    YELLOW: tuple = (255, 255, 0)
    CYAN: tuple = (0, 255, 255)
    MAGENTA: tuple = (255, 0, 255)
    ORANGE: tuple = (255, 165, 0)
    OFF: tuple = (0, 0, 0)


# named tuple for datetime representation
DateTime = collections.namedtuple(
    "DateTime", [
        "year",
        "month",
        "day",
        "weekday",
        "hour",
        "minute",
        "second",
        "millisecond"
    ]
)
