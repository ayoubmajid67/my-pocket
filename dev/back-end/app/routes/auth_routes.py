from flask import Blueprint, jsonify, request

from sqlalchemy import text
from app.routes.decorators.authDecorators import *

from app.utils.utile import generate_token 

from app.db import db; 
import app.utils.utile as Utile
import app.utils.authUtils.authUtils as authUtils

import os
import shutil
import bcrypt
import app.services.mailSever as mailServer
from datetime import datetime, timedelta
 
from app.utils.utile import *
from flask import request

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
     
    # Validate input fields
    data = request.get_json() or {}
    
    required_fields = {'Email', 'Password'}

    is_valid, missing_fields =Utile.validate_input(data, required_fields)
    
    if not is_valid:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    required_string_fields = {'Email', 'Password'}
    is_valid_string, missing_string_fields =Utile.are_all_strings(data,required_string_fields)
    if  not is_valid_string : 
        return jsonify({'error': f' invalid type fields types [int -> string!] : : {", ".join(missing_string_fields)}'}), 400
        
    email = data['Email'].strip().lower()
    password = data['Password'].strip()

    # Authenticate user by checking all relevant tables
    user_tables = ["Annonceur", "Etudiant", "Admin"]
    user, user_type = None, None
   
    for table in user_tables:
        user, user_type =authUtils.authenticate_user(email, password, table)
        if user:
            break

    # Handle authentication failure
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Check account status
    if user.get("Status") != 'active':
        return jsonify({'error': "Contact your administrator to activate your account!"}), 403
    
    
  
    server_ip,server_port = Utile.get_request_server_port(request) 
    profile_image_url = Utile.get_account_file_url(server_ip,server_port,user['Profile_Image'])
 
    # Generate and return token
    token = generate_token(user['Email'], user_type)
    response_data = {
        'message': "User logged in successfully",
        'token': token,
        'username': f"{user['Prenom']} {user['Nom']}",
        'profileImg': profile_image_url,
        'userType': user_type
    }
    return jsonify(response_data), 200



@auth_bp.route('/register', methods=['POST'])
def register():
    # Extract form data and files
    data = request.form.to_dict()
    files = request.files

    # Validate required fields
    required_fields = ['Email', 'Password', 'Account_type', 'Nom', 'Prenom', 'Telephone', 'Ville']
    
    is_valid, missing_fields =Utile.validate_input(data, required_fields)
    
    if not is_valid:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400


    is_valid_string, missing_string_fields =Utile.are_all_strings(data,required_fields)
    if  not is_valid_string : 
        return jsonify({'error': f' invalid type fields types [int -> string!] : : {", ".join(missing_string_fields)}'}), 400

    account_type = data.get('Account_type')
    if account_type not in ['Etudiant', 'Annonceur']:
        return jsonify({'error': 'Invalid account type'}), 400

    email = data['Email'].strip().lower()
    password = data['Password']

    # Check if user already exists
    check_query = text("""
        SELECT Email, 'Etudiant' AS user_type FROM Etudiant WHERE Email = :email
        UNION
        SELECT Email, 'Annonceur' AS user_type FROM Annonceur WHERE Email = :email
        UNION
        SELECT Email, 'Admin' AS user_type FROM Admin WHERE Email = :email
    """)
    existing_user = db.session.execute(check_query, {"email": email}).fetchone()
    if existing_user:
        return jsonify({'error': 'User with this email already exists'}), 409

    # Validate and save files based on account type
    server_ip,server_port = get_request_server_port(request)

    profile_image_file_name =   f"{email}_Profile_Image.webp"
    carteNationale_file_name =   f"{email}_CarteNationale.pdf"
    justificationDocument_file_name =   f"{email}_JustificationDocument.pdf"


   

    if account_type == 'Etudiant':
        required_files = ['JustificationDocument', 'CarteNationale']
        is_valid, missing_fields =Utile.validate_input(files, required_fields)

        if not is_valid :
            return jsonify({'error': f'Missing required files for Etudiant registration  {", ".join(required_files)}'}), 400

        # Validate file extensions
        for file_name in required_files:
            file = files[file_name]
            if not file.filename.lower().endswith('.pdf'):
                return jsonify({'error': f'{file_name} must be a PDF file'}), 400

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create user directory if it doesn't exist
        user_dir = os.path.join("data", "profiles", email)
        os.makedirs(user_dir, exist_ok=True)

        # Save files with the specified format
        file_data = {}
        for file_name in required_files:
            file = files[file_name]
            file_path = os.path.join(user_dir, f"{email}_{file_name}.pdf")
            file.save(file_path)
            file_data[file_name] = f"{email}_{file_name}.pdf"

        # Copy default profile image
        default_profile_path = os.path.join("data", "profiles", "default_profile.webp")
        user_profile_path = os.path.join(user_dir, f"{email}_Profile_Image.webp")
        shutil.copy(default_profile_path, user_profile_path)

        # Insert into Etudiant table
        insert_query = text("""
            INSERT INTO Etudiant (
                 JustificationDocument, CarteNationale, ConterInteret, Email, EtablissementScolaire, 
                Nom, Password, Prenom, Profile_Image, Telephone, Ville, Status,
                VerificationCode, VerificationCodeExpiration
            ) VALUES (
                 :JustificationDocument, :CarteNationale, :ConterInteret, :Email, :EtablissementScolaire,
                :Nom, :Password, :Prenom, :Profile_Image, :Telephone, :Ville, 'toVerify',
                :VerificationCode, :VerificationCodeExpiration
            )
        """)

        # Generate verification code and expiration time
        code = mailServer.generate_verification_code()
        expiration_time = datetime.utcnow() + timedelta(minutes=30)

        db.session.execute(insert_query, {
            "JustificationDocument": justificationDocument_file_name,
            "CarteNationale": carteNationale_file_name,
            "ConterInteret": data.get('ConterInteret'),
            "Email": email,
            "EtablissementScolaire": data.get('EtablissementScolaire'),
            "Nom": data['Nom'],
            "Password": hashed_password,
            "Prenom": data['Prenom'],
            "Profile_Image": profile_image_file_name,
            "Telephone": data['Telephone'],
            "Ville": data['Ville'],
            "VerificationCode": code,
            "VerificationCodeExpiration": expiration_time
        })
        db.session.commit()

    elif account_type == 'Annonceur':
        required_files = ['CarteNationale']
        is_valid, missing_fields =Utile.validate_input(files, required_files)


        if not is_valid :
            return jsonify({'error': f'Missing required files for Annonceur registration  {", ".join(missing_fields)}'}), 400

        # Validate file extensions
        for file_name in required_files:
            file = files[file_name]
            if not file.filename.lower().endswith('.pdf'):
                return jsonify({'error': f'{file_name} must be a PDF file'}), 400

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create user directory if it doesn't exist
        user_dir = os.path.join("data", "profiles", email)
        os.makedirs(user_dir, exist_ok=True)

        # Save files with the specified format
        file_data = {}
        for file_name in required_files:
            file = files[file_name]
            file_path = os.path.join(user_dir, f"{email}_{file_name}.pdf")
            file.save(file_path)
            file_data[file_name] = f"{email}_{file_name}.pdf"

        # Copy default profile image
        default_profile_path = os.path.join("data", "profiles", "default_profile.webp")
        user_profile_path = os.path.join(user_dir, f"{email}_Profile_Image.webp")
        shutil.copy(default_profile_path, user_profile_path)

        # Insert into Annonceur table
        insert_query = text("""
            INSERT INTO Annonceur (
                CarteNationale, Email, Nom, Password, Prenom, Profile_Image, Telephone, Ville, Status,
                VerificationCode, VerificationCodeExpiration
            ) VALUES (
                :CarteNationale, :Email, :Nom, :Password, :Prenom, :Profile_Image, :Telephone, :Ville, 'toVerify',
                :VerificationCode, :VerificationCodeExpiration
            )
        """)

        # Generate verification code and expiration time
        code = mailServer.generate_verification_code()
        expiration_time = datetime.utcnow() + timedelta(minutes=5)

        

        db.session.execute(insert_query, {
            "CarteNationale": carteNationale_file_name,
            "Email": email,
            "Nom": data['Nom'],
            "Password": hashed_password,
            "Prenom": data['Prenom'],
            "Profile_Image": profile_image_file_name,
            "Telephone": data['Telephone'],
            "Ville": data['Ville'],
            "VerificationCode": code,
            "VerificationCodeExpiration": expiration_time
        })
        db.session.commit()
        
 

    body=mailServer.create_email_body(code,data['Nom'])
    mailServer.send_email(email,body,"MyPocket:send the verification code")
    return jsonify({'message': 'Registration successful. Please verify your email.'}), 201


@auth_bp.route('/checkToken', methods=['POST'])
@token_required
def check_token(current_user):
     sanitized_user = {key : value for key,value in current_user.items() if key not in ['CarteNationale','Password']}
     server_ip,server_port = Utile.get_request_server_port(request) 
     profile_image_url = Utile.get_account_file_url(server_ip,server_port,sanitized_user['Profile_Image'])
     sanitized_user['Profile_Image']=profile_image_url

     return sanitized_user


@auth_bp.route('/verifyEmail', methods=['POST'])
def verify_email():
    data = request.get_json() or {}

    # Validate input
    required_fields=['Email','Code']

    
    is_valid, missing_fields =Utile.validate_input(data, required_fields)
    
    if not is_valid:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400


    is_valid_string, missing_string_fields =Utile.are_all_strings(data,required_fields)
    if  not is_valid_string : 
        return jsonify({'error': f' invalid type fields types [int -> string!] : : {", ".join(missing_string_fields)}'}), 400
    
    email = data.get('Email').strip()
    code = data.get('Code').strip()


    # Fetch the user from the database (select only necessary columns)
    check_query = text("""
        SELECT Email, VerificationCode, VerificationCodeExpiration, Status,Nom
        FROM Etudiant 
        WHERE Email = :email AND Status = :status
        
        UNION
        
        SELECT Email, VerificationCode, VerificationCodeExpiration, Status,Nom
        FROM Annonceur 
        WHERE Email = :email AND Status = :status
        
        UNION
        
        SELECT Email, VerificationCode, VerificationCodeExpiration, Status ,Nom
        FROM Admin 
        WHERE Email = :email AND Status = :status
    """)
    user = db.session.execute(check_query, {"email": email, "status": "toVerify"}).mappings().first()

    if not user:
        return jsonify({'error': 'User not found or already verified'}), 404

    # Convert the row object to a dictionary
    user = dict(user)

    # Compare the incoming code with the stored code
    if code != user.get("VerificationCode"):
        return jsonify({'error': 'Invalid verification code'}), 400

    # Check if the verification code has expired
    current_time = datetime.utcnow()
    if user.get("VerificationCodeExpiration") < current_time:
        return jsonify({'error': 'Verification code has expired. Please request a new one.'}), 400

    # Update the user's status to 'active'
    update_query_etudiant = text("""
        UPDATE Etudiant 
        SET Status = :status 
        WHERE Email = :email AND Status = :old_status
    """)
    update_query_annonceur = text("""
        UPDATE Annonceur 
        SET Status = :status 
        WHERE Email = :email AND Status = :old_status
    """)
    update_query_admin = text("""
        UPDATE Admin 
        SET Status = :status 
        WHERE Email = :email AND Status = :old_status
    """)

    rows_affected = 0
    if user["Status"] == "toVerify":
        if user["Email"] in [r[0] for r in db.session.execute(text("SELECT Email FROM Etudiant")).fetchall()]:
            rows_affected = db.session.execute(update_query_etudiant, {
                "email": email,
                "status": "toVerifyByAdmin",
                "old_status": "toVerify"
            }).rowcount
        elif user["Email"] in [r[0] for r in db.session.execute(text("SELECT Email FROM Annonceur")).fetchall()]:
            rows_affected = db.session.execute(update_query_annonceur, {
                "email": email,
                "status": "toVerifyByAdmin",
                "old_status": "toVerify"
            }).rowcount
        elif user["Email"] in [r[0] for r in db.session.execute(text("SELECT Email FROM Admin")).fetchall()]:
            rows_affected = db.session.execute(update_query_admin, {
                "email": email,
                "status": "toVerifyByAdmin",
                "old_status": "toVerify"
            }).rowcount

    if rows_affected == 0:
        return jsonify({'error': 'Failed to verify account'}), 500

    db.session.commit()
    
    body=mailServer.create_review_notification_body(user['Nom'])
    mailServer.send_email(user["Email"],body,"Account activation")


    return jsonify({'message': 'Account verified successfully, wait our team review in the next 24 hours to activate your account'}), 200  



@auth_bp.route('/resendCode', methods=['POST'])
def resend_code():
    data = request.get_json() or {}
    required_fields=['Email']
    is_valid, missing_fields =Utile.validate_input(data, required_fields)
    
    if not is_valid:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400


    is_valid_string, missing_string_fields =Utile.are_all_strings(data,required_fields)
    if  not is_valid_string : 
        return jsonify({'error': f' invalid type fields types [int -> string!] : : {", ".join(missing_string_fields)}'}), 400
    email = data.get('Email').strip()



    # Check if the user exists and has a `toVerify` status (select only necessary columns)
    check_query = text("""
        SELECT Email, VerificationCode, VerificationCodeExpiration, Status,Nom
        FROM Etudiant 
        WHERE Email = :email AND Status = :status
        
        UNION
        
        SELECT Email, VerificationCode, VerificationCodeExpiration, Status,Nom
        FROM Annonceur 
        WHERE Email = :email AND Status = :status
        
        UNION
        
        SELECT Email, VerificationCode, VerificationCodeExpiration, Status,Nom 
        FROM Admin 
        WHERE Email = :email AND Status = :status
    """)
    user = db.session.execute(check_query, {"email": email, "status": "toVerify"}).mappings().first()

    if not user:
        return jsonify({'error': 'User not found or already verified'}), 404

    # Convert the row object to a dictionary
    user = dict(user)

    # Ensure the user must wait 5 minutes before resending a new code
    current_time = datetime.utcnow()
    expiration_time = user.get("VerificationCodeExpiration")
    if expiration_time > current_time:
        time_remaining = (expiration_time - current_time).total_seconds() / 60
        return jsonify({
            'error': f'Please wait {time_remaining:.0f} minutes before requesting a new verification code.'
        }), 400

    # Generate and send a new verification code
    new_code = mailServer.generate_verification_code()
    new_expiration_time = current_time + timedelta(minutes=5)

    # Update the verification code and expiration time in the database
    update_query_etudiant = text("""
        UPDATE Etudiant 
        SET VerificationCode = :new_code, VerificationCodeExpiration = :new_expiration_time 
        WHERE Email = :email
    """)
    update_query_annonceur = text("""
        UPDATE Annonceur 
        SET VerificationCode = :new_code, VerificationCodeExpiration = :new_expiration_time 
        WHERE Email = :email
    """)
    update_query_admin = text("""
        UPDATE Admin 
        SET VerificationCode = :new_code, VerificationCodeExpiration = :new_expiration_time 
        WHERE Email = :email
    """)

    rows_affected = 0
    if user["Email"] in [r[0] for r in db.session.execute(text("SELECT Email FROM Etudiant")).fetchall()]:
        rows_affected = db.session.execute(update_query_etudiant, {
            "new_code": new_code,
            "new_expiration_time": new_expiration_time,
            "email": email
        }).rowcount
    elif user["Email"] in [r[0] for r in db.session.execute(text("SELECT Email FROM Annonceur")).fetchall()]:
        rows_affected = db.session.execute(update_query_annonceur, {
            "new_code": new_code,
            "new_expiration_time": new_expiration_time,
            "email": email
        }).rowcount
    elif user["Email"] in [r[0] for r in db.session.execute(text("SELECT Email FROM Admin")).fetchall()]:
        rows_affected = db.session.execute(update_query_admin, {
            "new_code": new_code,
            "new_expiration_time": new_expiration_time,
            "email": email
        }).rowcount

    if rows_affected == 0:
        return jsonify({'error': 'Failed to resend verification code'}), 500

    db.session.commit()

    # Send the new verification code via email
    body=mailServer.create_email_body(new_code,user['Nom'])
    mailServer.send_email(email,body,"MyPocket:Resend the verfication code")

    return jsonify({'message': 'Verification code resent successfully'}), 200


@auth_bp.route('/cancelVerifyEmail', methods=['DELETE'])
def cancel_verify():
    data = request.get_json() or {}


    required_fields=['Email']
    is_valid, missing_fields =Utile.validate_input(data, required_fields)
    
    if not is_valid:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400


    is_valid_string, missing_string_fields =Utile.are_all_strings(data,required_fields)
    if  not is_valid_string : 
        return jsonify({'error': f' invalid type fields types [int -> string!] : : {", ".join(missing_string_fields)}'}), 400
    
    email = data.get('Email').strip().lower()

    # Check if the user exists and has a `toVerify` status
    check_query = text("""
        SELECT Email, Status 
        FROM Etudiant 
        WHERE Email = :email AND Status = :status
        
        UNION
        
        SELECT Email, Status 
        FROM Annonceur 
        WHERE Email = :email AND Status = :status
    """)
    user = db.session.execute(check_query, {"email": email, "status": "toVerify"}).mappings().first()

    if not user:
        return jsonify({'error': 'User not found or already verified'}), 404

    # Delete the user from the respective table
    delete_query_etudiant = text("DELETE FROM Etudiant WHERE Email = :email AND Status = :status")
    delete_query_annonceur = text("DELETE FROM Annonceur WHERE Email = :email AND Status = :status")

    rows_affected = 0
    if user["Email"] in [r[0] for r in db.session.execute(text("SELECT Email FROM Etudiant")).fetchall()]:
        rows_affected = db.session.execute(delete_query_etudiant, {"email": email, "status": "toVerify"}).rowcount
    elif user["Email"] in [r[0] for r in db.session.execute(text("SELECT Email FROM Annonceur")).fetchall()]:
        rows_affected = db.session.execute(delete_query_annonceur, {"email": email, "status": "toVerify"}).rowcount

    if rows_affected == 0:
        return jsonify({'error': 'Failed to cancel verification'}), 500

    db.session.commit()

    return jsonify({'message': 'Account canceled successfully'}), 200