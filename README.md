# OLDI

OLDI - Open library database interface is a sqlite3 database managing GUI, aimed at increasing productivity and reliability for school libraries.

OLDI is written in python with the help of the sqlite3 and PyQt5 libraries. The database is stored locally.

# Reasons I made this

While participating at a volunteering event at our highschool, with the purpose of renovating the library, I have found that the librarian stores the books inside an excel spreadsheet(yeah, in an informatics-oriented highschool). 

I haven't really been able to find a tool that was simple enough to use, yet customised to the demands of our librarian. So I decided to make my own database interface.

# Reasons for the libraries that I use

## Sqlite3
I chose to use a local database, because I didn't really have a spare server to host an online database. Also, their FAQ bought me:
> For device-local storage with low writer concurrency and less than a terabyte of content, SQLite is almost always a better solution. SQLite is fast and reliable and it requires no configuration or maintenance. It keeps things simple. SQLite "just works". 

## DB-Api
DB-Api is a standard interface for Python database acces modules. This is what I use to talk from python to the sqlite database

## PyQt
PyQt is a python binding for the popular Qt cross-platform C++ GUI framework. This is what I used to design the User Interface, together with the Qt Designer app easily create custom widget using drag and drop default widgets.

## fbs
Fbs is a Python-based build tool for PyQt. I hade a breakthrough when I found that I could so easily package my python app into a Windows standalone .exe installer or a Linux .deb file. Neat stuff!

# Usage
The app consists of 3 main tabs: books, students and borrows.

![Books tab](https://github.com/nan-dre/OLDI/blob/master/Pictures/Books.png)
The books tab is just a list with all the books available in the database, color-coded with green/red if they are available or not.

![Students tab](https://github.com/nan-dre/OLDI/blob/master/Pictures/Students.png)
The students tab contains the students list. Double-clicking a student reveals more information about him and a way for him to borrow a book. Just fill in the book number and a coresponding borrow is created.

![Borrows tab](https://github.com/nan-dre/OLDI/blob/master/Pictures/Borrows.png)
The borrows tab contains the list with all the borrows. Double-clicking a borrow will mark the coresponding book as returned.

Each tab has searching and filtering capabilities, in order for the librarian to find the information she needs.

# Features
* Intuitive and minimalistic UI
* Fast database queries, even for lots of entries
* Capability to import excel files into the sqlite database

# What I have learned from this project
* Organizing of a book library data into an SQLite relational database
* UI development
* Basic oop usage and principles
* Patterns like Dependecy Injection etc
* Handling of big excel files, using the openpyxl module
* Usage of python @property decorators