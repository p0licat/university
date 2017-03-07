; @author: p0licat, 
;		   & Eric Rubl for integrating some fopen and printf C calls and debugging help as we were on a time limit.
;			
; 32 bit assembly program that searches
; for a string inside a file using the kmp ( Knuth-Morris-Pratt ) search algorithm.
;
; This program uses C function calls.
; The text file ( source ) should contain lines separated by \n
;


[bits 32]

section 	.text 	

extern  	_printf		; printf() 	C function
extern 		_exit		; exit() 	C function
extern 		_fgets		; fgets()	C function
extern 		_fopen		; fopen() 	C function
extern 		_scanf		; scanf()	C function
extern 		_getchar	; getchar() C function
extern 		_strlen		; strlen()	C function

global  	_main 		; main local function
global 		_generate_table ; generate_table local function
global 		_print_table	; print table local function ( debugging ) 
global 		_kmp			; kmp local function

; Performs a search on the [source] string, 
; looking for the [needle] string, using the Knuth-Morris-Pratt algorithm.
; Complexity: O(m+n) where m = strlen(source), n = strlen(needle)
; 
; This procedure relies on a pre-generated table of length n=strlen(needle), stored in [table].
; Output:
; 	modifies the eax register
; 	eax := pos, where pos is the index of the first occurence
; 	eax := -1 if no match is found in source
;
; This was mostly translated from a C implementation of the algorithm.
; Below or above the comments containing C code there are its respective ASM instructions.
_kmp:

	mov 	ecx, 0 ; m = 0
	mov 	edx, 0 ; i = 0
	
	parse_str:
		; if ( m + i > src_len ) 
		;     stop loop
		
		mov 	eax, ecx ; eax := m
		add 	eax, edx ; eax += i
		cmp		eax, [len_s] ; cmp(eax, len_s)
		
		; if ( m + 1 > src_len )

		jg		end_parse ; stop loop
		

		; if ( needle[i] == needle[m+i] )
		lea 	esi, [needle]
		add 	esi, edx ; esi -> needle[i]
		lea 	edi, [source]
		add 	edi, eax ; edi -> needle[m + i]
		cmpsb	; cmp(needle[i], needle[m+i])
		


		je 		first_case ; jump to first case
		jmp 	second_case ; else second_case


		first_case: ; needle[i] == needle[m+i]
			push 	ecx ; save ecx
			
			; if ( i == strlen(needle) - 1 )
			; 	return m;
			; i += 1
			
			mov 	ecx, [len]
			dec 	ecx
			cmp 	edx, ecx
			je 		return_case
			jmp 	continue_first_case

			return_case:
				pop 	eax ; pop m from stack ( ecx = m )
				ret
				
			continue_first_case:
			; end if

			pop 	ecx ; restore ecx
			inc 	edx
			jmp 	parse_str ; continue loop
			
		second_case: ; else
			lea 	edi, [table]
			add 	edi, edx
			mov 	eax, -1
			scasb

			;
			; if ( table[i] > -1 ) // first_subcase
			;	m += i - table[i], i = table[i]
			; else // second_subcase
			;	m += 1, i = 0
			;
			
			jl 		first_subcase   ; if ( table[i] > -1 )
			jmp 	second_subcase ; else
			
			first_subcase:
				lea 	esi, [table]
				add 	esi, edx
				mov 	eax, 0
				lodsb 	; eax := table[esi]
				add 	ecx, edx
				sub 	ecx, eax

				mov 	edx, eax
				jmp 	parse_str
			second_subcase:
				inc 	ecx
				mov 	edx, 0
				jmp 	parse_str
		
	end_parse: ; not found
	mov 	eax, -1
	ret


; Prints the generated table, for debugging purposes.
_print_table:
	lea 	esi,[table]
	mov 	ecx,[len]
	repeta2:
		lodsb
		cbw
		cwde
		push 	eax
		push 	DWORD format
		mov 	ebx,ecx
		call 	_printf
		mov 	ecx,ebx
		add 	esp,8
		loop 	repeta2
	ret
	
; Generates table used by KMP algorithm.
; Requires len to be initialized with the length of the needle.
;
_generate_table:
	lea 	edi, [table]
	mov 	eax, -1
	stosb 	; table[0] = -1
	mov 	eax, 0
	stosb 	; table[1] = 0
	
	mov 	ecx, 2    ; pos = 2
	mov 	edx, 0	  ; cnd = 0
	
	repeta:
		; while ( pos < length )
		cmp 	ecx,[len]
		jge 	end_table_loop ; stopping condition for loop

		; if ( pos >= length )
		;     end_loop
		
		
		lea 	esi, [needle]
		add 	esi, ecx
		dec 	esi
		lea 	edi, [needle]
		add 	edi, edx
		cmpsb
		; if ( needle[pos-1] == needle[cnd] )
		;      table_first_case
		je 	table_first_case
		
		cmp    edx,0
		; else if ( cnd )
		;     table_second_case
		ja    table_second_case
		
		;else
		;    table_third_case
		jmp    table_third_case
		
		
		table_first_case:
			inc 	edx
			lea 	edi,[table]
			add 	edi,ecx
			mov 	eax,edx
			stosb
			inc 	ecx
			; table[pos] = ++cnd, pos++;
			
		table_second_case:
			lea 	esi,[table]
			add 	esi,edx
			lodsb
			mov 	edx,eax
			; cnd = table[cnd];
			
		table_third_case:
			lea 	edi,[table]
			add 	edi, ecx
			mov 	eax,0
			stosb
			inc 	ecx
			jmp 	repeta
			; table[pos++] = 0;
		
	end_table_loop:		
	ret

_main: 
		
		; the first two scanf() calls ask the user for a filename, and a string to search for

		push 	DWORD filename ; push the filename onto stack
		push 	DWORD format_readfile ; push the readfile parameter for the scanf() function onto the stack
		call 	_scanf	; call the scanf function(). note that the C calling convention is used.
		add 	esp, 8	; restore the stack
		; scanf("%s", filename);
		
		push 	DWORD needle ; push the needle onto the stack
		push 	DWORD format_readfile ; push the readfile format...
		call 	_scanf	; call scanf
		add 	esp, 8	; restore the stack
		; scanf("%s", needle);
		

		push 	needle	; push needle to stack
		call 	_strlen	; and call strlen(needle)
		add 	esp, 4	; restore the stack
		mov 	[len], eax ; in order to store the needle's length in the len variable
		; len = strlen(needle)
		
		mov 	eax, 0	; clear
		mov 	ebx, 0	; registers
		mov 	ecx, 0	; modified by
		mov 	edx, 0	; function call
		; clear registers
		; and generate kmp table
		call 	_generate_table
		
		push 	DWORD mode ; 'r'
		push 	DWORD filename
		call 	_fopen	; call fopen 

		add 	esp, 8	; clear stack
		cmp 	eax, 0	; check for open error ( 0 ) 
		je 		openerr ; 0 is open error
		jmp 	open	; otherwise it's not an error
		; eax = fopen(filename, 'r');
		; if ( eax == NULL ) 
		;    error
		; ...
		
		
		openerr: ; error opening file
			push 	openerror	 ; push error message to stack
			call 	_printf		 ; call printf()
			add 	esp, 4		 ; clear stack
			jmp 	final		 ; end execution tree
			
		open:	; opened file
			mov 	[handler], eax	; move the handler (EAX) to the handler variable
			push 	DWORD handler	; push handler to stack	
			push 	handler_format	; and printing format for a handler
			call 	_printf			; and print the handler
			add 	esp, 8			; afterwards clear stack
			
			
		readline:
			push 	DWORD [handler]	; push handler
			push 	DWORD [bufsize]	; and buffersize
			push 	DWORD source	; and source file name
			call 	_fgets			; and call fgets with those
			add 	esp, 12			; clear stack
			; fgets(source, bufsize, handler)
			; i named these very oddly, the function works like this:
			; fgets(char* str, int num, FILE* stream);
			;
			;; so, source is the string that is read
			
			cmp 	eax, 0  ; if ( fgets(source, bufsize, handler) == NULL )
			je 		final   ; EOF
			
			push 	source	; get length of string that was read
			call 	_strlen	; with strlen()
			add 	esp, 4	; and clear stack
			dec 	AL ; and don't count the newline
			mov 	[len_s], eax ; store the length of the filename in the data segment
			; len_s = strlen(source)
			
			
			call 	_kmp ; eax = kmp()
			cmp 	eax, -1 ; kmp procedure returns -1 on eax if no match is found
			

			jne 	found_match ; if a match was found it is printed
			jmp 	no_match	; otherwise the execution continues
			
			
			found_match:
				push 	source	; print line
				push 	kmpform ; 
				call 	_printf
				add 	esp, 8
			no_match:
				jne readline ; loop back to read line, it will jump to final: label after EOF
			
		
		final:
			push 	0
			call 	_getchar ; trailing \n
			push 	0
			call 	_getchar ; trailing \n
			push 	0
			call 	_exit
			ret 

section .data	; data segment
; parameters for function calls
format_readfile:	db	'%s', 0 						 ; format_readfile	| 	parameter that scanf() uses in some calls 
handler_format: 	db	'Opened file handler: %s', 10, 0 ; handler_format 	| 	parameter that printf() uses in some calls

bufsize: 			dd 	1024	; bufsize 	| 	size of the read buffer for scanf
handler: 			dd 	1		; handler	| 	file handler will be stored here
filename: times 100 db 	0		; filename	| 	filename will be stored here ( max 100 bytes ) 
mode: 				db 	'r', 0	; mode		| 	parameter that scanf uses ( readmode )

; strings that can be printed
openerror: 			db 	'Open error!', 0 ; openerror 	|	string that can be passed to printf() in case of an error

; printf formats
kmpform: 			db 	'%s', 0xA, 0	 ; kmpform		| 	format for printf 
format: 			db 	'%d ',0			 ; format		| 	format for printf ( for printing integer )

; variable used internally
needle:	times 1024	db 	0	; string to search
source: times 1024 	db 	0	; line in which to search
len_s: 				dd 	11	; length of the source
table: times 1024 	db 	0	; 
len: 				dd 	0	; length of the needle


