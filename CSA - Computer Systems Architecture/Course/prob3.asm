;	Grup: 917
;	Nume: Bodica Septimiu-Calin
;	Prob: 1
;
;	1. Two byte strings are given ( s1 and s1 ). Construct string D by concatenating the elements from s1 from left to right and the elements from s2 from right to left.
; Example:
; S1: 	1, 2, 3, 4
; S2: 	5, 6, 7
; D: 	1, 2, 3, 4, 7, 6, 5

assume cs:code, ds:data

data segment
	s1 db 1, 2, 3, 4 ; offset 0 through 3
	len_s1 equ $-s1  ; len_s1 = 4 - 0 = 4
	s2 db 5, 6, 7	 ; offset 4 through 6
	len_s2 equ $-s2  ; len_s2 = 7 - 4 = 3
	D  db (len_s1 + len_s2) dup (?) ; 7 dup ?, offset 7 through 13
data ends

code segment
start:
	; Both registers ES and DS will be used.
	; This is because lod instructions use both.

	push 	data 	; push data to stack
	pop 	DS	; pop address of data segment into ds
	push 	data 	; push data to stack
	pop 	ES	; pop address of data segment into es, ES = DS = data
	
	lea 	si, s1 ; load effective address of s1 into si ( source index ) 
	lea 	di, D  ; load effective address of D  into di ( destination index ) 
	
	mov 	cx, len_s1 ; move into the counter register the length of s1 ( 4 ) 

	loop_s1:
		lodsb ; load into ax the value pointed to by si
		stosb ; move ax to the location pointed to by di

	loop 	loop_s1 ; loop cx times

	lea 	si, s2 + len_s2 - 1 ; s2 = 4, len_s2 = 3, 4 + 3 = 7, 7-1 = the last element of s2
	mov 	cx, len_s2 ; cx := 3

	loop_s2:
		std   	; set the direction flag ( <-- ) 
		lodsb 	; load into ax DS:[SI], SI is decremented ( DF = 1 )
		cld	; clear direction flag ( --> ) 
		stosb 	; move ax into DS:[DI], DI is incremented ( DF = 0 )
	loop 	loop_s2 ; loop 3 times
	
	mov 	ax, 4C00h
	int 	21h
code ends
end start
