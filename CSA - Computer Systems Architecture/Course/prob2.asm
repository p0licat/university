; 80x86 assembly code
; compiled with TASM and linked with TLINK 
; ( TURBO ASSEMBLER & TURBO LINKER )
; Emulated on DosBox
; Norton Guide as reference
;
; Gr:   917
; Nume: Septimiu-Calin Bodica
; Prob: 1
;
;	1. The words A and B are given. Obtain the word C in the following way:
;		- the bits 0-4 of C are the same as the bits 11-15 of A
;		- the bits 5-11 of C have the value 1
;		- the bits 12-15 of C are the same as the bits 8-11 of B 
       
assume cs:code, ds:data

data segment
    a 	dw 0FFFFh ; only bits of 1
    b 	dw 0FFFFh ; only bits of 1
    c 	dw ?	  ; result will be only bits of 1
data ends

code segment
start:   
    mov 	ax, data
    mov 	ds, ax      
    
    mov 	ax, a		  ; ax := FFFFh 
    and 	ah, 11111000b ; the most significant 5 bits of ah are masked
    and 	al, 0         ; al is cleared
            
    mov 	cl, 3		  ; we will perform 3 shifts
    ror 	ah, cl		  ; shift ah right 3 times, ah := 0001111b
    
    xchg 	al, ah		  ; swap al and ah, al = 0001111b, ah = 00000000b
    or 		dx, ax 		  ; and perform a logical or on dx to append the result
    
	or 		dh, 00001111b  ; using or
    or 		dl, 11110000b  ; we store only bits of 1 on the positions 5 to 11, the rest being unaffected
    
    mov 	ax, b		  ; ax := b ( FFFFh )
    and 	ah, 00001111b ; and keep only bits 8 to 11
	and 	al, 00000000b ; clear al
    mov 	cl, 4		  ; we will rotate 4 times
    rol 	ax, cl		  ; rotate left 4 times, ah = 11110000b
    
    or 		dx, ax		  ; append the result to dx with an or
    mov 	c, dx		  ; the desired value is now in dx, we move it to c, which is FFFFh
    
    mov 	ax, 4C00h
    int 	21h
code ends
end start
