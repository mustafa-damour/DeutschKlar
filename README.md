# DeutschKlar
German Study Group Matching App

#installation
0. creat new directory and make it current directory using cd:
1. setting a new python virtual (venv): environment, using the following command:
2. clone the repo into the new directory
3. activate venv using:

or use the following in Windows :

4. run
pip install -r requirements.txt

5. run flask server using

or in Windows:


## purpose of mock_up.py

to generate mock users and moderators if the db is released, this isn't a production feature.

## How I satisfied the project's requirements:

1.


## Admins and logs page

Admins has to be created as users first, then they are promoted by sys admin
via direct DB authorization, i.e. setting  is_admin to True in the DB

The DB in the repo contain an admin, with credentials:


In case of erasure of DB, a user has yo be promoted manually




## Funny chronicle 

when I created the footer, I loaded the html files and the server crashed, it turned to be an encoding problem, the problem was that :love: emoji needs a certain encoding, so we can say that Love crashed the system.













