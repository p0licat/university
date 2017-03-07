# console-travel
A console-based interface for searching places to travel.

# Origin
This project was done in 1h:30m for a  test at "Babes Bolyai" university in Cluj-Napoca, Cluj. 

# Screenshot
![Application Screenshot](http://i.imgur.com/dU1H0hG.png)

# Task 
Holidays Inc.
Create an application to help a tourism agency find holidays for its customers. The application will employ a layered architecture 
and will have a console-based user interface allowing its users to:
* 1.Search for holidays of a given type. The user will enter the type of the holiday and the program will display all holidays of the given type
ordered ascendingly by price (1p display list of holidays + 2 p if ordered by price).

* 2.Search  for  holidays  at  a  given  resort.  The user  will  enter  the  name  of  the  resort  and  the  program will display the list
of holidays at resorts whose names contain what the user entered as a substring (2p).

The  holidays  will  be  read  from  a  text  file  that  will  store  a minimum  of  10  holidays so  that  required functionalities  can  be  tested.  
Each  holiday  will  be  repr esented  by  one  line  in  the  file,  with format ```<id>,<resort name>,<type>,<price>```.
Ex.
* 1;Malaga;seaside;240
* 2;London;city

