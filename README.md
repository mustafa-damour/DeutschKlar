# DeutschKlar
German Study Group Matching Platform

#installation
0. creat new directory and make it current directory using cd:

1. setting a new python virtual (venv): environment, using the following command:

    `python -m venv /path/to/new/virtual/environment`

or in windows

    `python -m venv C:\path\to\new\virtual\environment`
2. clone the repo into the new directory

    `git clone git@github.com:mustafa-damour/DeutschKlar.git`
3. activate venv using:
Linux

    `source venv/bin/activate`

For Windows With CMD.

    `.\venv\Scripts\activate.bat`

For Windows With Power shell.

    `.\venv\Scripts\activate.ps1`

For Windows With Unix Like Shells For Example Git Bash CLI.

    `source venv/Scripts/activate`

    if it venv doesn't work in Windows run the following command:
    `Set-ExecutionPolicy RemoteSigned -Scope Process;`

4. install python libraries by running the following command in the project directory:

    `pip install -r requirements.txt`

5. run flask server using
    `flask –app server run`

or in Windows:
    `flask --app server run`


## purpose of mock_up.py

to generate mock users and moderators if the db is deleted, this isn't a production feature.
how to run it
    `python mockup_injection.py`

## How I satisfied the project's requirements:

1. The project is publically available on GitHub ✅
2. It uses Flask ✅
3. It uses at least one Python Standard library, I used datetime, secrets and json ✅
4. It contains a class with __init__ function (the class is Logger in logger.py), which logs into a logs file, to
be used in Admin's /logs page, it utilized 3 different functions. ✅
5. It makes use of localStorage, this is the form of 'suffix' key which is appended to the page's title, so 
the current logged use handle is written about on the tab, e.g. 'Home | @marco', the localStorage is cleared when
the user logs out. ✅
6. It uses modern JavaScript (for example, let and const rather than var). ✅
7. It makes use of the writing to and reading from the same file feature. This achieved with the Logger class methods
[log(), get_logs(), clear_logs(), get_last_n_logs()] ✅
8. It doesn't generate any error message even if the user enters a wrong input.✅
9. It lets the user enter a value in a text box at some point. This value should be received 
and processed by your back end Python code.✅
10. It is styled using CSS.✅
11. The code follows the code and style conventions we introduced in the course, is fully 
documented using comments and doesn't contain unused or experimental code. In 
particular, the code should not use print() or console.log() for any 
information the app user should see. Instead, all user feedback needs to be visible in 
the browser.✅


## Extra features

* Email service (Upon registeration and matchign with a study group)

## Admins and logs page

Admins has to be created as users first, then they are promoted by sys admin
via direct DB authorization, i.e. setting  is_admin to True in the DB

The DB in the repo contain an admin, with credentials:


In case of erasure of DB, a user has yo be promoted manually




## Funny chronicle 

when I created the footer, I loaded the html files and the server crashed, it turned to be an encoding problem, the problem was that :love: emoji needs a certain encoding, so we can say that Love crashed the system.













