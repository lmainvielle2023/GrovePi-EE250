import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Using physical pin 11 to blink an LED
GPIO.setmode(GPIO.BOARD)
chan_list = [11]
GPIO.setup(chan_list, GPIO.OUT)

# Hardware SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Set appropriate threshold levels after experimentation
lux_threshold = 500  # Example value, change this after experimentation
sound_threshold = 300  # Example value, change this after experimentation

light_sensor_channel = 0  # ADC channel for the light sensor
sound_sensor_channel = 1  # ADC channel for the sound sensor

while True:
    # Step 1: Blink the LED 5 times with on/off intervals of 500ms
    for _ in range(5):
        GPIO.output(11, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(11, GPIO.LOW)
        time.sleep(0.5)

    # Step 2: Read the light sensor for 5 seconds at 100 ms intervals
    start_time = time.time()
    while time.time() - start_time < 5:
        light_value = mcp.read_adc(light_sensor_channel)
        if light_value > lux_threshold:
            print(f"Light reading: {light_value} - bright")
        else:
            print(f"Light reading: {light_value} - dark")
        time.sleep(0.1)

    # Step 3: Blink the LED 4 times with on/off intervals of 200ms
    for _ in range(4):
        GPIO.output(11, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(11, GPIO.LOW)
        time.sleep(0.2)

    # Step 4: Read the sound sensor for 5 seconds at 100 ms intervals
    start_time = time.time()
    while time.time() - start_time < 5:
        sound_value = mcp.read_adc(sound_sensor_channel)
        print(f"Sound reading: {sound_value}")
        if sound_value > sound_threshold:
            # If tapped, turn on LED for 100 ms
            GPIO.output(11, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(11, GPIO.LOW)
        time.sleep(0.1)

# Clean up GPIO pins when the loop is exited (though this loop runs infinitely)
GPIO.cleanup()