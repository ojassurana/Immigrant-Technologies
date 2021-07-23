from flask import Flask, redirect, url_for, render_template, request
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()


client = pymongo.MongoClient(os.getenv('MONGO_CLIENT')) #This takes the login credientials for the mongoDB from the .env file e.g. "mongodb+srv://ojas:<PASSWORD>@cluster0.kfpcm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
db = client.get_database('UserData')
Information_Collection = db.get_collection("Information")
Items = [ "Oxygen Cylinder", "Hospital Bed",  "Plasma",  "Remedisvir",  "Fabiflu", "Tocilizumbad", "Oxygen Refill","All Items"]
application = Flask(__name__)

@application.route("/", methods = ["POST","GET"])  #Landing page 
def home():
	return render_template("index.html")
	
@application.route("/find",methods =  ["POST","GET"]) # when the submit button is pressed 
def find():
	recipients = []
	# The data extraction from the form
	donations = request.form["Donation"] 
	location = request.form["Location"]

	#Choice of data extract 
	if donations == "All Items" and location =="All Locations":
		out = Information_Collection.find()
		for i in out:
			if len(i) == 5:
				recipients.append(i)
		if recipients == []:
			return render_template("nil.html")
		return render_template("results.html",recipients = recipients, donation = 8 ,location="All Locations",items = Items)
	
	if donations == "All Items":
		out = Information_Collection.find({"Location":{"$eq":location}})
		for i in out:
			if len(i) == 5:
				recipients.append(i)
		if recipients == []:
			return render_template("nil.html")
		return render_template("results.html",recipients = recipients, donation = 8 ,location=location,items = Items)
	
	if location == "All Locations":
		donation = Items.index(donations) +1
		out = Information_Collection.find({"Item":{"$eq":donation}})
		for i in out:
			if len(i) == 5:
				recipients.append(i)
		if recipients == []:
			return render_template("nil.html")
		return render_template("results.html",recipients = recipients, donation = donation ,location="All Locations",items = Items)

	
	donation = Items.index(donations)+1 # finds the index of the item 
	out = Information_Collection.find( {"$and":[{"Item":{"$eq":donation}},{"Location":{"$eq":location}}]}   ) # Data retreival from the main database           


	#Data parsing of the raw output to prepare for front end code 
	for i in out:
		if len(i) == 5:
				recipients.append(i)
	if recipients == []: #If there is no match then this list will be empty  
		return render_template("nil.html")
	return render_template("results.html",recipients = recipients, donation = donation ,location=location,items = Items)
	
	
if __name__ == "__main__":


	application.run(debug=True)
