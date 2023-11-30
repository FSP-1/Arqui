import time
import RPi.GPIO as GPIO

# Definimos el pin GPIO al que está conectado cada botón.
button_left_pin = 26
button_right_pin = 5

# Desactivamos las posibles advertencias de que el GPIO ya está en uso.
# Suelen salir cuando cerramos un script sin limpiar los GPIO, pero no importa.
GPIO.setwarnings(False)
# Utilizamos numeración BCM para los pines, correspondiente a las etiquetas de la Figura 1.
GPIO.setmode(GPIO.BCM)

# Definimos los pines de los botones como entradas.
# Utilizamos resistencias pull-down por software para que los pines devuelvan 0 
# cuando los botones no estén pulsados y los pines estén, por lo tanto, flotando.
GPIO.setup(button_left_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_right_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Esta función se llamará cada vez que se dispare un evento de pulsación de botón.
# El evento pasa como argumento a la funcion callback el pin que lo ha disparado.
def button_callback(pin):
    if pin == button_left_pin:
        print('Ha pulsado el botón izquierdo.')
    elif pin == button_right_pin:
        print('Ha pulsado el botón derecho.')

# Añadimos los eventos de cada pulsador. Queremos que se dispare el evento en el flanco de subida
# de la señal, ya que vamos a cortocircuitar VCC. Configuramos un debouncing de 200 milisegundos.
GPIO.add_event_detect(button_left_pin, GPIO.RISING, callback=button_callback, bouncetime=200)
GPIO.add_event_detect(button_right_pin, GPIO.RISING, callback=button_callback, bouncetime=200)

# Toda la gestión de los pulsadores la hacemos mediante eventos, 
# así que dejamos este bucle infinito para que el programa no se cierre.
while True:
    time.sleep(1)
