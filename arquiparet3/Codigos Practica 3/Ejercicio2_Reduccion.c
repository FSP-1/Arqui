#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

unsigned int n = 20;
unsigned int n_threads = 1;
unsigned int *A;
unsigned long long result = 0;

pthread_t *threads;
pthread_mutex_t lock;

// Imprime el vector entero si es pequeño, o parte de él si es grande.
void print_vec(unsigned int *V, const char *name, unsigned int n) {
    printf("%s = [", name);
    if (n > 20) {
        for (unsigned int i = 0; i < 5; i++) {
            printf("%d, ", V[i]);
        }
        printf("..., ");
        for (unsigned int i = n - 5; i < n; i++) {
            printf("%d", V[i]);
            if (i < n - 1) {
                printf(", ");
            }
        }

    } else {
        for (unsigned int i = 0; i < n; i++) {
            printf("%2d", V[i]);
            if (i < n - 1) {
                printf(", ");
            }
        }
    }
    printf("]\n");
}

// Calcula la parte del vector que le toca a cada thread. Devuelve índices [start, end).
void get_partition(unsigned int tid, unsigned int *start, unsigned int *end) {
    float split = n/(float)n_threads;
    *start = tid*split;
    *end = (tid + 1)*split;
    // Si queda un elemento de resto, se lo damos al último thread.
    if (tid == n_threads - 1 && *end < n) {
        *end = n;
    }
}

// Inicializamos el vector con los n primeros números naturales.
void *init_vector(void *args) {
    unsigned int tid = (unsigned int) args;
    unsigned int start, end;
    get_partition(tid, &start, &end);

    for (unsigned int i = start; i < end; i++) {
        A[i] = i+1;
    }
}

// Reducción, calcula la parte que le toca a cada thread y suma todos los elementos.
void *reduce_sum(void *args) {
    unsigned int tid = (unsigned int) args;
    unsigned int start, end;
    get_partition(tid, &start, &end);

    printf("Hilo %2d reduce el rango de índices [%d, %d): %d elementos\n", tid, start, end, end - start);

    unsigned long long partial_result = 0;
    for (unsigned int i = start; i < end; i++) {
        partial_result += A[i];
    }
    
    
    // Sumamos nuestro resultado parcial al resultado global
    pthread_mutex_lock(&lock);
    result += partial_result;
    pthread_mutex_unlock(&lock);
}

void launch_threads(void *function) {
    // Lanzamos n_threads en paralelo.
    for (unsigned int i = 0; i < n_threads; i++) {
        int tid = i;
        pthread_create(&threads[i], NULL, function, (void *) i);
    }
    // Esperamos a que todos los threads hayan acabado.
    for (unsigned int i = 0; i < n_threads; i++) {
        pthread_join(threads[i], NULL);
    }
}


int main(int argc, char **argv) {

    // El primer argumento debe ser el número de valores.
    if (argc > 1) {
        n = atoi(argv[1]);
    }
    printf("Número de valores: %u\n", n);

    // El segundo argumento debe ser el número de hilos.
    if (argc > 2) {
        n_threads = atoi(argv[2]);
    }
    printf("Número de threads: %u\n", n_threads);

    // Reservamos memoria para A y los punteros a los threads.
    A = (unsigned int *) malloc(n*sizeof(unsigned int));
    threads = (pthread_t *) malloc(n_threads*sizeof(pthread_t *));

    // Inicializamos A con los n primeros números naturales.
    launch_threads(init_vector);
    print_vec(A, "Vector a reducir", n);

    // Creamos el mutex que necesitaremos para sincronizar las reducciones parciales.
    pthread_mutex_init(&lock, NULL);

    // Lanzamos n_threads para reducir el vector en paralelo.
    launch_threads(reduce_sum);
    printf("Resultado de la reducción: %llu\n", result);

    free(A);
    free(threads);
    pthread_mutex_destroy(&lock);

    // Comprobamos el resultado con la fórmula.
    unsigned long long check = (unsigned long long) n*(n+1)/2;
    if (result == check) {
        printf("Correcto :)\n");
        return EXIT_SUCCESS;
    } else {
        printf("Erróneo, debería ser %llu :(\n", check);
        return EXIT_FAILURE;
    }

    return 0;
}
