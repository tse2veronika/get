import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
pins = list(reversed([22, 27, 17, 26, 25, 21, 20, 16]))
GPIO.setup(pins, GPIO.OUT)
dynamic_range = 3.131
def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f'Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В')
        print('Устанавливаем 0.0 В')
        return 0
    return int(voltage / dynamic_range * 255)

def number_to_dec(number):
    b = [int(elem) for elem in bin(number)[2:].zfill(8)]
    GPIO.output(pins, b)

try:
    while True:
        try:
            voltage = float(input('Введите напряжение в Вольтах: '))
            number = voltage_to_number(voltage)
            number_to_dec(number)
        except ValueError:
            print('Вы ввели не то число. Попробуйте еще раз\n')
finally:
    GPIO.output(pins, 0)
    GPIO.cleanup()
