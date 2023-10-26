.macro myPUSH, a @Definimos una macro PUSH para rpis
sub sp,sp,#4
str \a,[sp]
.endm


.macro myPOP, a
ldr \a,[sp]
add sp,sp,#4
.endm



.text
.global Menor
Menor:  myPUSH r4  @inicio de la rutina Menor
	myPUSH lr
	cmp r0, r1
	blt Ret2
	mov r0, r1
Ret2:   myPOP lr
	myPOP r4
	bx lr	     		@fin de la rutina Menor
