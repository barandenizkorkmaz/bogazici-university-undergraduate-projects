code segment  

read:
	mov ah,01h
	int 21h
	mov ah,0
	mov cx,ax	; cx = the character read.
	
main:
	cmp cx,13d    ; checking if the character read = 'Enter'
	je end_of_scan_path    ; finish the reading process.	
	
	;;;;;;;;;;;;;;;operations
	cmp cx,2bh    ; checking if the character read = '+'.
	je addition	  ; jump to addition label.
	
	cmp cx,2ah    ; checking if the character read = '*'.
	je multiplication    ; jump to multiplication label.
	
	cmp cx,2fh    ; checking if the character read = '/'
	je division    ; jump to division label.
	
	cmp cx,26h    ; checking if the character read = '&'(bitwise and).
	je bwand    ; jump to bwand label.
	
	cmp cx,7ch    ; checking if the character read = '|'(bitwise or).
	je bwor    ; jump to bwor label.
	
	cmp cx,5eh    ; checking if the character read = '^'(bitwise xor).
	je bwxor    ; jump to bwxor.
	;;;;;;;;;;;;;;operations
	
	cmp cx,20h    ; checking if the character read = ' '(space)
	jne int_process
	
	jmp prereset    ; jump to prereset if the character read is not space.
	jmp read    ; continue reading.
	
prereset:
	cmp dx, 0	; checking if dx = 0 which mean if there is still a number that is being written.
	je reset
	jmp read
	
addition:
	pop bx	; popping the last number.
	pop ax	; popping the second last number.
	add ax,bx	; addding the two them up.
	push ax    ; pushing the result onto the stack.
	mov bx, 0	; restores the bx register.  
	mov dx, 1 ; indicates that the last character written is an operation character.
	jmp read
	
multiplication:
	pop bx	; popping the last number.
	pop ax	; popping the second last number.
	mul bx  ; multiplying them
	push ax	  ; pushing the result onto the stack.
	mov bx, 0    ; restores the bx register.
	mov dx, 1 	 ; indicates that the last character written is an operation character.
	jmp read
	
division: 
	mov dx,0	; resets the dx register to avoid unexpected result during division.
	pop bx    ; popping the last number.
	pop ax	  ; popping the second last number.
	div bx	  ; dividing the value in ax by the value in bx.
	push ax	  ; pushing the result onto the stack.
	mov bx, 0  ; restores the bx register.
	mov dx, 1  ; indicates that the last character written is an operation character.
	jmp read

end_of_scan_path: ; an intermediate label before jumping to the end_of_scan label.
	pop ax	; popping the final result
	mov cx,4d   ; setting the counter to 4.
	jmp end_of_scan

bwand:
	pop bx	 ; popping the last number.
	pop ax	 ; popping the second last number.
	and ax, bx  ; 'and'ing them(bitwise).
	push ax	   ; pushing the result onto the stack.
	mov bx, 0 ; restores the bx register.
	mov dx, 1 ; indicates that the last character written is an operation character.
	jmp read
bwor:
	pop bx   ; popping the last number.
	pop ax   ; popping the second last number.
	or ax, bx  ; 'or'ing them(bitwise). 
	push ax   ; pushing the result onto the stack.
	mov bx, 0 ; restores the bx register.
	mov dx, 1 ; indicates that the last character written is an operation character.
	jmp read
bwxor:
	pop bx   ; popping the last number.
	pop ax	 ; popping the second last number.
	xor ax, bx  ; 'xor'ing them(bitwise). 
	push ax   ; pushing the result onto the stack.
	mov bx, 0 ; restores the bx register.
	mov dx, 1 ; indicates that the last character written is an operation character.
	jmp read

int_process:
    cmp cx,65d	 ; checking the value of the character read.
    jge letter_process ; if it is greater than 65, which means it is a letter, jump to letter_process
    
    sub cx,48d	; subtracting 48 from the value in cx which is a number, to store it as it is in the register.
    mov ax,bx   ; moving the current value to the ax register.
    mov dx,16	; storing a constant in the dx register for multiplication.
    mul dx   ; multiplying the value in ax with the value in dx(=16) to store the current number correctly. 
    mov bx,ax   ; storing the result in the bx register.
    add bx,cx   ; adding the last digit of the number to the current number.
    jmp read
    
reset:
    push bx   ; pushing the result onto the stack.
    mov bx,0   ; restoring the bx register.
	jmp read    
	
letter_process:  ; the same as the int_process label, only difference is that 55 is subtracted from the value in the cx register, indicating that it is a letter.
    sub cx,55d  
    mov ax,bx  
    mov dx,16
    mul dx 
    mov bx,ax
    add bx,cx
    jmp read	

end_of_scan:
	mov dx, 0	; resetting the dx register for storage.
	mov bx, 10h	 ; storing 16 in the bx register.
	div bx	; dividing the result by 16.
	
	cmp dl, 9h	; checking the remainder part(whether it is greater or less than 9) to find out whether it is a digit or letter.
	jle zero_to_9
	jmp A_to_F

zero_to_9:	
	add dl, 30h   ; adding 55 to the value to store the ascii value of the digit.
	push dx		; pushing the value to the stack.
	mov dx, 0h   ; resetting the dx register for the next division.
	dec cx	; decrementing the counter by one.
	jnz end_of_scan ; continuing dividing if cx is not zero.
	mov cx, 4d   ; storing 4 in the cx register.
	mov ax, 0d   ; resetting the ax register.
	jmp check_zeros

A_to_F:   ; the same as the zero_to_9 label, the only difference is 37 is added to the value in the dx register.
	add dl, 37h
	push dx
	mov dx, 0h
	dec cx
	jnz end_of_scan
	mov cx, 4d
	mov ax, 0d
	jmp check_zeros

check_zeros:
	cmp cx, 0h	; checking the counter(if it is zero or not).
	je is_all_zero
	pop dx	; popping a digit from the stack.
	dec cx	; decrementing the counter by one.
	cmp dx, 30h	 ; checking if the digit is zero.
	je check_zeros   ; if it is zero, stay in the loop.
	push dx   ; if the digit is not zero, push it onto the stack to pop and display later.
	inc cx   ; incrementing cx by one to undo what is done above.
	jmp display 
	
is_all_zero: ; displays just zero in the console if all the digits popped from the stack are zero.
	mov ah, 02h
	int 21h
	jmp exit
	
display:  ; displays the digits one by one.
	cmp cx,0h
	je exit
	pop dx
	dec cx
	mov ah, 02h
	int 21h
	jmp display
exit:
	int 20h
code ends