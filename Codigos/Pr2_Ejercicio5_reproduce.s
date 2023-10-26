.macro myPUSH, a  @Definimos una macro PUSH para rpi
sub sp,sp,#4
str \a,[sp]
.endm

.macro myPOP, a  	@Definimos una macro POP para rpi
ldr \a,[sp]
add sp,sp,#4
.endm



.text
.global reproduce
reproduce: myPUSH r5
         myPUSH r6
         myPUSH r7
         myPUSH lr
         mov r6,r2 @DirReproductor = reproduccion de cada sonido de la cancion se activa cuando se escribe la palabra correspondiente de la cancion en esa direccion
sonido: cmp r0,r1
        bgt return
        ldr r5,[r0]
        str r5, [r6] @ se reproduce esa palabra de la cancion con el sonido correspondiente en el dispositivo reproductor
        add r0,#4
        b sonido
return:	cmp r0,r1
        subeq r0,r0,r0
         myPOP lr
         myPOP r7
         myPOP r6
         myPOP r5
         bx lr
