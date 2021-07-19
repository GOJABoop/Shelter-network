# Shelter-network
Project to introduce the use of relational databases using Python and PostgreSQL

## About this project
Simple software developed with the Python Tkinter library to introduce the design and implementation of a relational database with PostgreSQL.

The problem is the following:
A network of dog shelters wants to keep a record of shelters, sponsors, volunteers, dogs, adoptions and adopters, 
each shelter will store their identification and address. For sponsors, you want to save your ID, name, and phone number. 
For the dog help program where each volunteer wants to save their volunteer ID, first name, last name, date of birth, 
registration date and phone number, for dogs you want to store dog code, breed, age, name, entry of date and know if it has been adopted, 
for adoptions adoption code, adoption date, dog identification, shelter identification as well as identification of the adopter, 
for the adopters their name, address and telephone number will be saved.

Each shelter has its own volunteers, dogs, adoptions, and adopters, as each shelter has its own for sponsors, but sponsors can sponsor more than one shelter.

## How to execute
Install Python as well as PostgreSQL, create the database with the tables and triggers in the file "shelters.sql", 
you should also change the data in the header of the file "red_refugios.pyw" (connection to the database).
