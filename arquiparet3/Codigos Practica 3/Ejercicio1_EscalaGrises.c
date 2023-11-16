#include <stdio.h>
#include <time.h>
#include "ppm.h"

// Devuelve el tiempo en milisegundos desde un punto desconocido del pasado.
// Haciendo la diferencia entre dos valores podemos saber el tiempo de cómputo de un trozo de código.
double get_time_ms() {
    struct timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) == 0) {
        return ts.tv_sec * 1000 + ts.tv_nsec / 1000000.0;
    } else {
        return 0;
    }
}

// Convierte una imagen de tres canales de color por píxel (RGB) a escala de grises.
// No se asusten por la calidad de este código, esta rutina está programada subóptimamente 
// para que la mejoremos durante la futura Práctica 5 :)
void color2gray(Image *color_img, Image *gray_img) {
    // Leemos el primer canal (rojo) y calculamos su contribución.
    for (int x = 0; x < color_img->width; x++) {
        for (int y = 0; y < color_img->height; y++) {
            unsigned int gray_offset = y*color_img->width + x;
            unsigned int rgb_offset = gray_offset * 3;
            unsigned char r = color_img->data[rgb_offset];
            gray_img->data[gray_offset] = 0.21f*r;
        }
    }

    // Leemos el segundo canal (verde) y calculamos su contribución.
    for (int x = 0; x < color_img->width; x++) {
        for (int y = 0; y < color_img->height; y++) {
            unsigned int gray_offset = y*color_img->width + x;
            unsigned int rgb_offset = gray_offset * 3;
            unsigned char g = color_img->data[rgb_offset + 1];
            gray_img->data[gray_offset] += 0.71f*g;
        }
    }

    // Leemos el tercer canal (azul) y calculamos su contribución.
    for (int x = 0; x < color_img->width; x++) {
        for (int y = 0; y < color_img->height; y++) {
            unsigned int gray_offset = y*color_img->width + x;
            unsigned int rgb_offset = gray_offset * 3;
            unsigned char b = color_img->data[rgb_offset + 2];
            gray_img->data[gray_offset] += 0.07f*b;
        }
    }
}


int main(int argc, char **argv) {
    char *color_img_filename = (char *) "Alcazaba.ppm";
    if (argc > 1) {
        color_img_filename = argv[1];
    }
    
    double start_time = get_time_ms();
    Image *color_img = ImageRead(color_img_filename);
    double elapsed_time = get_time_ms() - start_time;
    printf("Tiempo de lectura de la imagen: %.6f ms\n", elapsed_time);

    printf("Imagen de entrada: %s (%d x %d x %d)\n", color_img_filename, color_img->width, color_img->height, color_img->channels);
    Image *gray_img = ImageCreate(color_img->width, color_img->height, 1);

    start_time = get_time_ms();
    color2gray(color_img, gray_img);
    elapsed_time = get_time_ms() - start_time;
    printf("Tiempo de cómputo de la imagen: %.6f ms\n", elapsed_time);

    char *gray_img_filename = (char *)"ResultadoGris.ppm";
    printf("Imagen de salida: %s (%d x %d x %d)\n", gray_img_filename, gray_img->width, gray_img->height, gray_img->channels);
    
    start_time = get_time_ms();
    ImageWrite(gray_img, gray_img_filename);
    elapsed_time = get_time_ms() - start_time;
    printf("Tiempo de escritura de la imagen: %.6f ms\n", elapsed_time);

    return 0;
}
