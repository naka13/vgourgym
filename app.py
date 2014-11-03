from flask import Flask, request, make_response, redirect, session, json, g
from flask.ext.sqlalchemy import SQLAlchemy
import os
import pdb


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
#api_key = app.config.get("SECRET_KEY")


from models import *


def generate_response(status, result, message):
	response = {}
	response["status"] = status
	response["result"] = result
	response["message"] = message
	return json.dumps(response)


@app.route("/")
def home():
	return "homepage"


@app.route("/gym", methods=["GET"])
def gym():

	if request.method == "GET":
		key = request.args.get("Api-Key")
		if key is None:
			response = generate_response("403", {}, "No key provided.")

		elif key != app.config.get("SECRET_KEY"):
			response = generate_response("403", {}, "You are not authorized!")

		else:
			gym_id = request.args.get("gym_id")
			if gym_id is None:
				response = generate_response("400", {}, "Bad request. No gym id provided")
			else:
				entry = db.session.query(Gym).filter(Gym.id == gym_id).first()
				pdb.set_trace()
				response = generate_response("200", {"about":entry.about, "timings":entry.timings, "location":entry.location}, "")

	elif request.method == "POST":
		headers = request.headers
		data = request.data
		try:
			api_key = str(headers["Api-Key"])
			content_type = str(headers["Content-Type"])
			body = json.loads(data)
			about = body["about"]
			timings = body["timings"]
			location = body["location"]
			if (about is None) or (about.strip() == ""):
				response = generate_response("400", {}, "Bad request. No 'about' specified")
			elif (timings is None) or (timings.strip() == ""):
				response = generate_response("400", {}, "Bad request. No timings specified")
			elif (location is None) or (location.strip() == ""):
				response = generate_response("400", {},"Bad request. No location specified")
			else:
				new_gym = Gym(about=about, timings=timings, location=location)
				db.session.add(new_gym)
				db.session.commit()
				response = json.dumps(new_gym)

		except ValueError, KeyError:
			response = generate_response("400", {}, "Bad Request. Provide Content-Type, Api-Key in request header and/or body in json format")

	else:
		response = generate_response("404", {}, "Not Found!")

	return response





def dbinit():
	db.create_all()
	db.session.commit()


if __name__ == "__main__":
	dbinit()
	app.run()
