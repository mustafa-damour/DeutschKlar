from flask import Flask
from flask_sse import sse
from apscheduler.schedulers.background import BackgroundScheduler
import random

# from server import app
# import server




app = Flask(__name__)
app.config["REDIS_URL"]="redis://172.17.0.2"


app.register_blueprint(sse, url_prefix='/events')



def get_data():
    data = list()
    data.append({'name': fake.name()})
    return data

def server_side_event():
    with app.app_context():
        sse.publish(get_data(), type='customer')
        print("New Customer Time: ",datetime.datetime.now())
   

sched = BackgroundScheduler(daemon=True)
sched.add_job(server_side_event,'interval',seconds=10, id ="myJob")
sched.start()