#include <stdio.h>

void reproduce(int *INI,int *FIN, int *DirReproductor); // Declaración de la funcion que hemos definido en ensamblador

void main(int argc,char **argv){
int N=15; /* Definimos una canción de 15 sonidos*/
int A[15]={7,5,0,9,7,5,4,-1,-1,0,3,4,6,9,11};
int Reproductor[1]={0};
int t,i,globalmin;
for (i =0;i<=N;i++){
	reproduce(&A[0],&A[14],&Reproductor[0]);
printf("El primer sonido de A es %d\n",A[i]);
}
}
