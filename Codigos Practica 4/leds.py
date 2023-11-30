import time
import RPi.GPIO as GPIO

# Definimos el pin GPIO al que está conectado cada LED.
led_left_pin = 19
led_middle_pin = 13
led_right_pin = 6

# Desactivamos las posibles advertencias de que el GPIO ya está en uso.
# Suelen salir cuando cerramos un script sin limpiar los GPIO, pero no importa.
GPIO.setwarnings(False)
# Utilizamos numeración BCM para los pines, correspondiente a las etiquetas de la Figura 1.
GPIO.setmode(GPIO.BCM)

# Definimos los tres pines de los tres LEDs como salidas.
GPIO.setup(led_left_pin, GPIO.OUT)
GPIO.setup(led_middle_pin, GPIO.OUT)
GPIO.setup(led_right_pin, GPIO.OUT)

delay = 0.3
while True:    
    GPIO.output(led_left_pin, GPIO.HIGH);
    GPIO.output(led_middle_pin, GPIO.HIGH);
    GPIO.output(led_right_pin, GPIO.HIGH);
    time.sleep(delay)

    GPIO.output(led_right_pin, GPIO.LOW);
    time.sleep(delay)
    GPIO.output(led_middle_pin, GPIO.LOW);
    time.sleep(delay)
    GPIO.output(led_left_pin, GPIO.LOW);
    time.sleep(delay)
