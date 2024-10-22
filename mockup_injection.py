from crud import initialize_groups, generate_cities_persons, CITIES
from model import Moderator, User

initialize_groups()

generate_cities_persons(role=Moderator, cities=CITIES)

for i in range(3):
    generate_cities_persons(role=User, cities=CITIES)
