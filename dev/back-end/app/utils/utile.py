import jwt
from flask import current_app
from datetime import datetime, timedelta
import re

from flask import current_app



def generate_token(email, account_type="Etudiant", expirationDays=30):
    if account_type=="Admin" : expirationDays=1
    payload = {
        'email': email,
        'account_type': account_type,
        'exp': datetime.utcnow() + timedelta(days=expirationDays)  # Token expires in 1 hour
    }
    print("the payload :",payload['exp'])
    token = jwt.encode(
        payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token


def validate_fields(data, required_fields):
    missing_fields = [
        field for field in required_fields
        if field not in data or (isinstance(data[field], str) and not data[field].strip())
    ]
    return missing_fields



def validate_password(password):
    """
    Validates a password based on the following rules:
    1. At least 8 characters long.
    2. Contains at least one digit (0-9).
    3. Contains at least one special character (e.g., !@#$%^&*).
    4. Can start with any character (letter, number, or special character).
    """
    password_regex = r'^(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$'
   
    return re.match(password_regex, password) is not None


def validate_password(password):
    # Example: Password must be at least 8 characters, contain at least one number, one uppercase letter, and one special character
    password_regex = r'^(?=.*[0-9])(?=.*[!@#$%^&*().?/])[a-zA-Z0-9!@#$%^&*().?/]{6,}$'
    return re.match(password_regex, password) is not None


def are_all_strings(data,required_string_data):
    not_string_field = [field for field in  required_string_data if   not isinstance(data[field],str)] 
    return not not_string_field,not_string_field


def allowed_file_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_IMG_EXTENSIONS"]


def allowed_file_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_VIDEO_EXTENSIONS"]


def validate_input(data, required_fields):
    missing_fields = [field for field in required_fields if  field not in data or  (isinstance(data[field],str) and  not data[field].strip())]
    return not missing_fields, missing_fields


import bcrypt
def hash_password(password):
    # Encode the password to bytes (required by bcrypt)
    password_bytes = password.encode('utf-8')
    
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)


    # Return the hashed password
    return hashed_password.decode('utf-8')  # Decode to string for easier handling




def check_hashed_password(password,hashedPassword):
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashedPassword.encode('utf-8')
    return bcrypt.checkpw(password_bytes,hashed_password_bytes)

#  $2b$12$oTbnMglRvVkav3Om8cwKDuHl8SoDCOhvsgtB/jUnIR9J5tmG2WZNG



def get_request_server_port(request):
    server_ip = request.host.split(':')[0]
    server_port = request.host.split(':')[1] if ':' in request.host else '80'
    return server_ip, server_port

def get_account_file_url(server_ip,server_port,file_name) :
    return f"http://{server_ip}:{server_port}/api/{current_app.config['API_VERSION']}/accounts/file/{file_name}"


def get_product_img_url(server_ip,server_port,image_name,product_id) :
    return f"http://{server_ip}:{server_port}/api/{current_app.config['API_VERSION']}/productsOffers/{product_id}/file/{image_name}"


def get_housing_offer_img_url(server_ip,server_port,image_name,housing_offer_id) :
    return f"http://{server_ip}:{server_port}/api/{current_app.config['API_VERSION']}/housingOffers/{housing_offer_id}/file/{image_name}"
