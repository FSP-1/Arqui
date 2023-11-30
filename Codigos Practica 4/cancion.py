import sys, time
import RPi.GPIO as GPIO

buzzer_pin = 21
led_left_pin = 19
led_middle_pin = 13
led_right_pin = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(led_left_pin, GPIO.OUT)
GPIO.setup(led_middle_pin, GPIO.OUT)
GPIO.setup(led_right_pin, GPIO.OUT)

# Frecuencias (aproximadas) en Hz de las notas
la3  = 220 # A3
si3  = 247 # B3
do4  = 262 # C4
re4  = 294 # D4
mi4  = 330 # E4
fa4  = 349 # F4
sol4 = 392 # G4
la4  = 440 # A4
si4  = 494 # B4
do5  = 523 # C4
sil  = 0   # Silencio

# Definimos las notas que componen la canción y la duración de cada nota.
cancion = [mi4, si3, do4, re4, do4, si3, la3, la3, do4, mi4, re4, do4, si3, do4, re4, mi4, do4, la3, la3]
tempo   = [10, 5, 5, 10, 5, 5, 10, 5, 5, 10, 5, 5, 15, 5, 10, 10, 10, 10, 10]
dutycycle = 1

# Vamos a utilizar modulación por pulso (PWM) para hacer música con el zumbador :)
buzzer = GPIO.PWM(buzzer_pin, 100)
buzzer.start(0)

for note, duration in zip(cancion, tempo):
    print('Reproduciendo frecuencia {:3d} Hz con tempo {}.'.format(note, duration))
    if note == sil:
        buzzer.ChangeDutyCycle(0)
    else:
        buzzer.ChangeFrequency(note)
        buzzer.ChangeDutyCycle(dutycycle)

    GPIO.output(led_left_pin, GPIO.HIGH);
    GPIO.output(led_middle_pin, GPIO.HIGH);
    GPIO.output(led_right_pin, GPIO.HIGH);
    time.sleep(duration/50)

    GPIO.output(led_left_pin, GPIO.LOW);
    GPIO.output(led_middle_pin, GPIO.LOW);
    GPIO.output(led_right_pin, GPIO.LOW);
    time.sleep(duration/50)
    
buzzer.stop()
GPIO.cleanup()
