from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..models.user import User
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import user_db
from app import restful_api, app
from app.exceptions import UserNotFoundException
from ..decorators.security import admin_or_self_required, admin_required

class UsersSearchApi(Resource):
	decorators = [jwt_required(optional= True)]	#Add appropriate decorators
	def get(self, email):
		#log the email as info
		if not email:
			return {'message': 'Mandatory parameter email not found in reques'}, 400
		conn = get_db_connection()
		user = user_db.get_user_details_from_email(conn, email)
		if not user:
			#add error log stating that the user was not found in DB
			return {'message': f'User (email) not found in DB'}
		identity_email = get_jwt_identity()
		if identity_email:
			return user.to_json()	
		else:
			#log warning that anonymous user is accessing the data
			return {'name': user.name, 'email': user.email}
		#pass #Add logic to give full user details if accesed by a user with valid token else return just name and email

# Uncomment the below line by adding a valid url mapping for the user search API
restful_api.add_resource(UsersSearchApi, '/api/users/email/<string:email>')