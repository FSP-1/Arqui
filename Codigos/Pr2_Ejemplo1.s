.data
N: .word 8
A: .word 7,5,0,9,7,4,5,-1
Min: .word 0
imprime:  .asciz "El mínimo global es %d\n" @ comenta en ARMSim y descomenta en Raspberry

.text
.global main
main:
	push {r6,r7,r8,r9,r10,lr}	@Inicio rutina main
	ldr r9,=N
	ldr r7,[r9]  			@r7-->N
	ldr r8,=A
	ldr r10,[r8] 			@r10-->globalmin=A[0],ini.mínimo global
mov r6, #1 				@r6=1 inicializa contador
	mov r9,#4  				@r9=4 inicializa desplazamiento
loop: 	cmp r6,r7   			@j<N ejecuta el bucle
	bge fin
	ldr r0,[r8,r9] 			@r0-->A[j]
	mov r1,r10 				@r1=Mínimo global=globalmin
	bl Menor  				@Menor(A[j],globalmin)
	mov r10,r0  				@r0 y r10 tienen el mínimo global
	add r9,r9,#4   			@r9=r9+4 (para acceder al siguiente elemento del vector)
	add r6,r6,#1 			@j=j+1
	b loop
fin:
	ldr r9,=Min
	str r10,[r9]				@guarda el minimo global en dir. Min
	 @ Estas lineas se comentan en ARMSim y descomentan en Raspberry
	  mov r1,r0				@pasamos globalmin al segundo argumento de printf
         ldr r0,=imprime
         bl printf 	       		@ llamo a función printf

	pop {r6,r7,r8,r9,r10,lr}		@fin rutina main
	bx lr					@retorno del control al sistema


Menor: 	push {r4,lr}  		@inicio de la rutina Menor
	cmp r0, r1
	blt Ret2
	mov r0, r1
Ret2: 	pop {r4,lr}				@fin de la rutina Menor
	bx lr	     				@retorno del control a main
