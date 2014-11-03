from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


gyms_facilities = db.Table("gyms_facilities",										##helper table for gyms and facilities association
    db.Column("gym_id", db.Integer, db.ForeignKey("gyms.id")),						##should be table, NOT class
    db.Column("facility_id", db.Integer, db.ForeignKey("facilities.id"))
)


gyms_programs = db.Table("gyms_programs",
	db.Column("gym_id", db.Integer, db.ForeignKey("gyms.id")),
	db.Column("program_id", db.Integer, db.ForeignKey("programs.id"))
)


programs_members = db.Table("programs_members",
	db.Column("program_id", db.Integer, db.ForeignKey("programs.id")),
	db.Column("member_id", db.Integer, db.ForeignKey("members.id"))
)


gyms_classes = db.Table("gyms_classes",
	db.Column("gym_id", db.Integer, db.ForeignKey("gyms.id")),
	db.Column("class_id", db.Integer, db.ForeignKey("classes.id"))
)


class Gym(db.Model):
	__tablename__ = "gyms"

	id = db.Column(db.Integer, primary_key=True)
	about = db.Column(db.Text)														##text field
	timings = db.Column(db.String())												##can have multiple start times and as many end times.
	location = db.Column(db.Text())													##text field
	
	members = db.relationship("Member", backref="gym",
                                lazy="dynamic")										##relationships are one to many by default
																					##backref would allow person.gym query
																					##load data dynamically
	
	gyms_facilities = db.relationship("Facility", secondary=gyms_facilities,		##many-to-many relationship. dynamic backref
        backref=db.backref("gyms", lazy="dynamic"))

	gyms_programs = db.relationship("Program", secondary=gyms_programs,				##many-to-many relationship. dynamic backref
        backref=db.backref("gyms", lazy="dynamic"))

	trainers = db.relationship("Trainer", backref="gym",							##one to many relationship
									lazy="dynamic")

	gyms_classes = db.relationship("Class", secondary=gyms_classes,
		backref=db.backref("gyms", lazy="dynamic"))


	def __init__(self, about, timings, location):									##initializer
		self.about = about
		self.timings = timings
		self.location = location


	def __repr__(self):																##representation
		return "<id {}>".format(self.id)





class Member(db.Model):
	__tablename__ = "members"

	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String())												##string field, no limitation on length
	last_name = db.Column(db.String())												##string field, no limitation on length
	number = db.Column(db.String(10), unique=True)									##string field with length 10
	gym_id = db.Column(db.Integer, db.ForeignKey("gyms.id"))

	galleries = db.relationship("Gallery", backref="member",
									lazy="dynamic")


	def __init__(self, first_name, last_name, number, gym_id):						##initializer
		self.first_name = first_name
		self.last_name = last_name
		self.number = number
		self.gym_id = gym_id

	def __repr__(self):																##representation
		return "<id {}>".format(self.id)





class Facility(db.Model):
	__tablename__ = "facilities"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	description = db.Column(db.Text)


	def __init__(self, name, description):
		self.name = name
		self.description = description


	def __repr__(self):
		return "<id {}>".format(self.id)






class Program(db.Model):
	__tablename__ = "programs"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	description = db.Column(db.Text)
	price = db.Column(db.Float)
	start_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)

	programs_members = db.relationship('Member', secondary=programs_members,				##many-to-many relationship. dynamic backref
        backref=db.backref('programs', lazy='dynamic'))


	def __init__(self, name, description, price, start_date, end_date):
		self.name = name
		self.description = description
		self.price = price
		self.start_date = start_date
		self.end_date = end_date


	def __repr__(self):
		return "<id {}>".format(self.id)





class Trainer(db.Model):
	__tablename__ = "trainers"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	details = db.Column(db.Text)
	gym_id = db.Column(db.Integer, db.ForeignKey("gyms.id"))


	def __init__(self, name, gym_id):
		self.name = name
		self.gym_id = gym_id


	def __repr__(self):
		return "<id {}>".format(self.id)





class Class(db.Model):
	__tablename__ = "classes"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	details = db.Column(db.Text)
	start_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)
	start_time = db.Column(db.DateTime)
	end_time = db.Column(db.DateTime)
	price = db.Column(db.Float)


	def __init__(self, name, details, start_date, end_date, start_time, end_time, price):
		self.name = name
		self.details = details
		self.start_date = start_date
		self.end_date = end_date
		self.start_time = start_time
		self.end_time = end_time
		self.price = price


	def __repr__(self):
		return "<id {}>".format(self.id)




class Gallery(db.Model):
	__tablename__ = "galleries"

	id = db.Column(db.Integer, primary_key=True)
	member_id = db.Column(db.Integer, db.ForeignKey("members.id"))

	images = db.relationship("Image", backref="gallery",
								lazy="dynamic")


	def __init__(self, member_id):
		self.member_id = member_id


	def __repr__(self):
		return "<id {}>".format(self.id)





class Image(db.Model):
	__tablename__ = "images"

	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(100))
	gallery_id = db.Column(db.Integer, db.ForeignKey("galleries.id"))


	def __init__(self, url, gallery_id):
		self.url = url
		self.gallery_id = gallery_id


	def __ref__(self):
		return "<id {}>".format(self.id)