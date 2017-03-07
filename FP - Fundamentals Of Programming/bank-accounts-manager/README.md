# Account Manager

Homework Project for "[Babes Bolyai](http://www.cs.ubbcluj.ro/en/)" [University](http://www.cs.ubbcluj.ro/en/). This bank account manager has a simple console-based UI and allows the user
to add transactions, modify them, calculate a total balance and undo/redo operations.

# Screenshtot
![Application Screenshot](http://i.imgur.com/g917gRC.png?1)

# Interface
As you can see from the screenshot, the UI is similar to that of a shell command line. It takes user input and uses the regex library to validate it.

```python
        "add": r"^\s*add\s*([0-9]+),\s*([a-zA-Z]+),\s*\"(.*)\"\s*$",
		"insert": r"^\s*insert ([0-9]+),\s*([0-9]+),\s*([a-zA-Z]+),\s*\"(.+)\"\s*$",
		"help": r"^\s*help\s*$",
		"greater than": r"^\s*greater\s*than\s*([0-9]+)\s*$",
		"less than": r"^\s*less\s*than\s*([0-9]+)\s*$",
		"all": r"^\s*all\s*([a-z]*)\s*",
		"balance": r"^\s*balance\s*([0-9]*)\s*",
		"filter": r"^\s*filter\s*([a-z]+)\s*([0-9]*)\s*",
```

# Task
John wants to manage his bank account. In order to complete this task, John needs an application to store, 
for a certain month, all the banking transactions which were performed on his account. Each transaction will
be stored in the application through the following elements: day (of the month in which the transaction was made), 
amount of money transferred into/from the account, the type of the transaction 
(into the account – in or from the account - out), and description of the transaction. 
