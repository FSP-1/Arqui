#include <stdio.h>
#include <stdlib.h>

// Declaración de la funcion que hemos definido en ensamblador
void reproduce (int *inicio, int *fin, int *DirReproductor);

int main (int argc, char *argv[]) {

    int n_canciones = 8; // Número de canciones
    int n_sonidos = 16;  // Número de sonidos por canción

    // Reservamos una zona de memoria para el dispositivo de reproducción.
    int *DirReproductor = (int *) malloc(sizeof(int));
    // Reservamos una zona de memoria para los sonidos de todas las canciones.
    int *DatosCanciones = (int *) malloc(n_canciones*n_sonidos*sizeof(int));
    // Reservamos una zona de memoria para los punteros a la posición 
    // de memoria del primer y último sonido de cada canción.
    int **ListaReproduccion = (int **) malloc(n_canciones*2*sizeof(int *));
    
    printf("Inicializando canciones...\n");
    for (int i = 0; i < n_canciones; i++) {
        if(i==2){
            // Calculamos los punteros al primer y último sonido de la canción
            ListaReproduccion[2*i]   = &DatosCanciones[i*n_sonidos];
            ListaReproduccion[2*i + 1] = &DatosCanciones[(i+1)*n_sonidos - 1];

            // Generamos sintéticamente los sonidos de la canción
            for (int j = 0; j < n_sonidos; j++) {
                DatosCanciones[i*n_sonidos + j] = (i+1)*100 + j;
            }

            // Para comprobar, imprimimos el resultado
            printf("[Canción %d] \n  Dirección primer sonido: %p \n  Dirección último sonido: %p\n", i + 1, ListaReproduccion[2*i], ListaReproduccion[2*i+1]); 
            printf("  Datos de sonido: ");
            // Recorremos los sonidos, esta vez utilizando los punteros que hemos 
            // precalculado anteriormente.
            for (int *p = ListaReproduccion[2*i]; p <= ListaReproduccion[2*i + 1]; p++) {
                printf("%d ", *p);
            }
            printf("\n");
        }
    }
            reproduce(ListaReproduccion[2*2], ListaReproduccion[2*2 + 1] ,DirReproductor);

    // EJERCICIO: Añada el código necesario para reproducir la canción número 3
    // utilizando la rutina "reproduce" en ensamblador. Modifique la rutina reproduce
    // para que se impriman por pantalla los sonidos correspondientes a la canción.
    

    return 0;
}

