from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse
import bcrypt
from django.db import models
import re
from django.contrib import messages
from django.db.models import Q
from datetime import date, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


class UserManager(models.Manager):
	def registeration(self, name, alias, email, password, confirm_password, bday):
		errors = []
		errors.append(self.validate_length(name, 'name', 2, 'Name is too short'))
		errors.append(self.validate_length(alias, 'alias', 2, 'Alias is too short'))
		errors.append(self.validate_email(email))
		errors.append(self.validate_passwords(password, confirm_password))
		errors.append(self.validate_dob(bday))
		error = []

		for elements in range(0, len(errors)):
			try:
				error.append(errors[elements][1])
			except:
				pass
		error2 = {}
		for d in error:
			error2.update(d)

		if not bool(error2):
			pw_bytes = password.encode('utf-8')
			hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
			Register.objects.create(name = name, alias = alias,
			password = hashed, email = email, poked = 0)
			success = {}
			success['success'] = "Registeration comeplete, please log in"
			return (True, success)
		else:
			return (False, error2)

	def validate_dob(self, bday):
		date = ""
		try:
			date = datetime.strptime(bday, '%Y-%m-%d')
		except:
			errors = {}
			errors["dob"] = "Date of Birth needs to be in formate mm/dd/yyy"
			return(False, errors)

		if date > datetime.now():
			errors = {}
			errors["dob"] = "You cannot be from the future"
			return(False, errors)

	def login(self, email, password):
		errors = {}
		valid = True
		try:
			registered = Register.objects.get(email = email)
		except:
			errors['email'] = "Email Not found"
			valid = False

		if(valid):
			pw_bytes = password.encode('utf-8')
			salt = registered.password.encode('utf-8')
			
			if bcrypt.hashpw(pw_bytes, salt) != salt:
				errors['password'] = "Email and password do not match"
				return (False, errors)
			else: 
				return (True, Register.objects.get(email=email))
		else:
			return (False, errors)


	def validate_length(self, test, name, alength, error_string):
		errors = {}
		if len(test) < alength:
			errors[name] = error_string
			return(False, errors)

	def validate_email(self, email_address):
		errors = {}
		if not EMAIL_REGEX.match(email_address):
			errors['email'] = "Please enter a valid email"
			return(False, errors)

	def validate_passwords(self, password, confirm_password):
		errors = {}
		if password != confirm_password:
			errors['password'] = "Passwords do not match"
			return(False, errors)
		elif len(password) < 8:
			errors['password'] = "Passwords need to be longer than 8 characters"
			return(False, errors)


	def get_all(self, email):
		return(True, Register.objects.filter(~Q(email=email)))

	def get_user(self, email):
		return(True, Register.objects.get(email = email))

	def user_poked(self, email):
		test = Register.objects.get(email = email)
		test2 = len(Poking.objects.filter(got_poked = test.id))
		return(True, test2)

	def user_poked_total(self, email):
		reg = Register.objects.get(email = email)
		test = Poking.objects.filter(got_poked = reg.id)
		return(True, Poking.objects.filter(got_poked = reg.id))

	def get_poked(self, id):
		return(True, Register.objects.get(id = id))

	def update(self, times, id):
		reg = Register.objects.get(id = id)
		reg.poked = times
		reg.save()
		return(True)

	def create(self, id, email):
		reg2 = Register.objects.get(id = id)
		reg = Register.objects.get(email = email)
		try:
			poke = Poking.objects.filter(who_poked = reg, got_poked = reg2.id)
			poking = poke[0].poked
			poking += 1
			Poking.objects.filter(who_poked = reg, got_poked = reg2.id).update(poked =poking)
		except:
			Poking.objects.create(who_poked = reg, poked =1, got_poked =reg2.id)
		return True


# Create your models here.
class Register(models.Model):
	name = models.CharField(max_length=45)
	alias = models.CharField(max_length=45)
	password = models.TextField(max_length=1000)
	email = models.EmailField()
	poked = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	userManager = UserManager()
	objects = models.Manager()

class Poking(models.Model):
	who_poked = models.ForeignKey(Register)
	poked = models.IntegerField()
	got_poked = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)



