#include <stdio.h>

//int Menor(int a,int b){
//if (a<b) b=a;
//return b;
//}
int Menor(int a,int b); // Declaración de la funcion que hemos definido en ensamblador

void main(int argc,char **argv){
int N=8;
int A[8]={7,99,100,58,-7,4,5,1};
int t,i,globalmin;
globalmin=A[0];
for(i=1;i<8;i++){
	globalmin=Menor(A[i],globalmin);
}

printf("El mínimo global es %d\n",globalmin);
}
