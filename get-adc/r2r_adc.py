import RPi.GPIO as GPIO
import time
class R2R_ADC:
    def __init__(self, dynamic_range,compare_time, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        b = [int(elem) for elem in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, b)

    def sequential_counting_adc(self):
        for k in range(256):
            self.number_to_dac(k)
            time.sleep(self.compare_time)
            comparator_output = GPIO.input(self.comp_gpio)
            if comparator_output == 1:
                return k
        return 255

    def get_sc_voltage(self):
        value = self.sequential_counting_adc()
        value = (value / 255) * self.dynamic_range
        return value

    def successive_approximation_adc(self):
        left = 0
        right = 256
        value = 0
        while (right - left) > 1:
            value = (left + right) // 2
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                right = value
            else:
                left = value
        return value
    def get_sar_voltage(self):
        value = self.successive_approximation_adc()
        value = (value / 255) * self.dynamic_range
        return value

if __name__ == '__main__':
    try:
        r2r_adc = R2R_ADC(3.3, 0.01)
        while True:
            voltage = r2r_adc.get_sar_voltage()
            print(f'Напряжение: {voltage} В')
    finally:
        r2r_adc.deinit()
