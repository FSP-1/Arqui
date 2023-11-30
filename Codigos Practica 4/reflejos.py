import sys, time, random
from enum import Enum
from datetime import datetime
import RPi.GPIO as GPIO

# Definimos los pines de todos los componentes.
button_left_pin = 26
button_right_pin = 5
led_left_pin = 19
led_middle_pin = 13
led_right_pin = 6
buzzer_pin = 21

# Guardamos el estado actual de cada LED: 0 apagado, 1 encendido.
led_left_status = 0
led_middle_status = 0
led_right_status = 0

# En esta clase definimos la información que vamos a guardar de cada jugador
class Player:
    def __init__(self, name, button_pin, led_pin):
        self.name = name
        self.ready = False
        self.score = 0
        self.button = button_pin
        self.led = led_pin
        self.pushed = False

# Este enum define los diferentes estados por los que pasa el bucle del juego.
class GameState(Enum):
    WAITING = 1 # Esperando jugadores (paso 1 en el guión)
    FIRING = 2  # Listo y disparando (paso 2)
    FIRED = 3   # Disparado y esperando (paso 3)
    POST = 4    # La partida ha acabado (paso 5)

# Activa un pin por una duración dada, la usamos para dar un pitido.
def beep(pin, duration):
    GPIO.output(pin, GPIO.HIGH);
    time.sleep(duration)
    GPIO.output(pin, GPIO.LOW);

# Esta función muestra el marcador y resetea la partida.
# Se llama al comienzo del programa y un segundo después de que alguien gane.
def reset_game():
    global state
    print('MARCADOR: {}: {}, {}: {}\n'.format(
        left_player.name, left_player.score, right_player.name, right_player.score))
    print('Esperando jugadores, pulse el boton cuando esté preparado...')
    state = GameState.WAITING
    left_player.ready = False
    left_player.pushed = False
    right_player.ready = False
    right_player.pushed = False

# Esta función se llamará cada vez que se dispare un evento de pulsación de botón.
# El evento pasa como argumento a la funcion callback el pin que lo ha disparado.
def button_callback(pin):
    global state, left_player, right_player

    # Determinamos el jugador que ha pulsado el botón a partir del pin que se ha utilizado.
    player = None
    if pin == button_left_pin:
        player = left_player;
    elif pin == button_right_pin:
        player = right_player;

    # Si estamos esperando jugadores, marcamos como listo al jugador que haya pulsado.
    if state == GameState.WAITING:
        if player.ready:
            print('[{}] Se impacienta.'.format(player.name))
        else: 
            print('[{}] Está listo.'.format(player.name))
            player.ready = True

    # Si estamos en medio de una partida pero todavía no se ha apagado la luz, el jugador 
    # ha pulsado prematuramente, le restamos un punto y reseteamos la partida.
    elif state == GameState.FIRING:
        print('[{}] Pulsó antes de tiempo, se le resta un punto.'.format(player.name))
        player.score -= 1
        reset_game()
        beep(buzzer_pin, 0.05)
        time.sleep(0.05)
        beep(buzzer_pin, 0.05)

    # Si ya se ha apagado la luz, el primer jugador que pulse y llegue aquí, gana :)
    elif state == GameState.FIRED:
        state = GameState.POST
        elapsed = datetime.now() - firing_time
        print('[{}] Ganó pulsando en {:.0f} milisegundos.'.format(player.name, elapsed.total_seconds() * 1000))
        player.score += 1

    # Si el segundo jugador pulsa antes de un segundo después del vencedor mostraremos su velocidad,
    # para que pueda ver qué tan lejos ha quedado de ganar.
    elif state == GameState.POST and not player.pushed:
        elapsed = datetime.now() - firing_time
        print('[{}] Perdió pulsando en {:.0f} milisegundos.'.format(player.name, elapsed.total_seconds() * 1000))

    if state == GameState.FIRED or state == GameState.POST:
        player.pushed = True
        player.led = GPIO.output(pin, GPIO.HIGH);
        # COMPLETAR: Cuando un jugador pulse durante la partida, su LED (definido por player.led) 
        # debe encenderse (GPIO.HIGH).


# Desactivamos las posibles advertencias de que el GPIO ya está en uso.
# Suelen salir cuando cerramos un script sin limpiar los GPIO, pero no importa.
GPIO.setwarnings(False)
# Utilizamos numeración BCM para los pines, correspondiente a las etiquetas de la Figura 1.
GPIO.setmode(GPIO.BCM)

# COMPLETAR: Defina los componentes que faltan: El botón derecho y los LEDs.
GPIO.setup(button_left_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_right_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(led_left_pin, GPIO.OUT)
GPIO.setup(led_middle_pin, GPIO.OUT)
GPIO.setup(led_right_pin, GPIO.OUT)

# COMPLETAR: Añada los eventos para ambos botones. Queremos que se disparen en el flanco de subida,
# utilicen como callback la función button_callback y tengan un debouncing de 200 milisegundos.
GPIO.add_event_detect(button_left_pin, GPIO.RISING, callback=button_callback, bouncetime=200)
GPIO.add_event_detect(button_right_pin, GPIO.RISING, callback=button_callback, bouncetime=200)

# Definimos los dos jugadores: Su nombre, su pulsador y su LED.
# COMPLETAR: Cambie los nombres de los jugadores por los de los miembros del grupo.
left_player = Player('Maria', button_left_pin, led_left_pin)
right_player = Player('Franco', button_right_pin, led_right_pin)

firing_time = None
reset_game()

GPIO.output(led_left_pin, GPIO.HIGH);
GPIO.output(led_middle_pin, GPIO.HIGH);
GPIO.output(led_right_pin, GPIO.HIGH);

while True:
    
    # Estamos esperando que los jugadores estén listos.
    if state == GameState.WAITING:
        GPIO.output(left_player.led, not left_player.ready);
        GPIO.output(right_player.led, not right_player.ready);

        # Si ambos jugadores están listos
        if left_player.ready and right_player.ready:
            # COMPLETAR: Deje el LED central encendido fijamente.
            led_middle_status= 1
            beep(buzzer_pin, 0.05)
            state = GameState.FIRING
        else:
            # COMPLETAR: Si los jugadores no están listos, el LED central debe parpadear cada 0.2 s.
            GPIO.output(led_middle_pin, GPIO.HIGH);
            time.sleep(0.2)
            GPIO.output(led_middle_pin, GPIO.LOW);
            time.sleep(0.2)

    # Los jugadores están listos y comienza la partida.
    elif state == GameState.FIRING:
        print('Comienza la partida, pulse cuando se apague la luz...')
        # Calculamos el tiempo que va a pasar hasta que se apague la luz.
        firing_delay = random.uniform(1, 5)
        time.sleep(firing_delay)

        # Volvemos a comprobar en caso de que algún jugador haya pulsado antes de tiempo
        # mientras estábamos en sleep y la partida haya acabado ya.
        if state == GameState.FIRING:
            firing_time = datetime.now()
            state = GameState.FIRED
            # COMPLETAR: Ha pasado el tiempo de disparo, apague el LED central para indicarlo.
            led_middle_status= 1
            print('¡Pulse! El led tardó {:.2f} segundos en apagarse.'.format(firing_delay))

    # Si la partida ha acabado, en dos segundos reseteamos y volvemos a empezar.
    elif state == GameState.FIRED or state == GameState.POST:
        time.sleep(1)
        if state == GameState.POST:
            time.sleep(1)
            reset_game()
