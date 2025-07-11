from flask import jsonify, request, current_app
import jwt
from sqlalchemy import text
from functools import wraps


from app.db import db; 


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get the token from the Authorization header  dddd
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode the JWT token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            
            # Initialize variables
            current_user = None
            user_type = None
            
            # Check if the user exists in the Etudiant table
            StudentCheckQuery = text('SELECT * FROM Etudiant WHERE Email = :email')
            etudiant_result = db.session.execute(StudentCheckQuery, {"email": data["email"]}).mappings().first()
            if etudiant_result:
                current_user =dict(etudiant_result)
            
            # If not found in Etudiant, check Admin table
            if not current_user:
                AdminCheckQuery = text('SELECT * FROM Admin WHERE Email = :email')
                admin_result = db.session.execute(AdminCheckQuery, {"email": data["email"]}).mappings().first()
                if admin_result:
                    current_user =dict(admin_result)
                   
            
            # If not found in Admin, check Annonceur table
            if not current_user:
                AnnonceurCheckQuery = text('SELECT * FROM Annonceur WHERE Email = :email')
                annonceur_result = db.session.execute(AnnonceurCheckQuery, {"email": data["email"]}).mappings().first()
                if annonceur_result:
                    current_user =dict(annonceur_result)
            
            # If no user is found, return an error
            if not current_user:
                return jsonify({'error': 'User not found!'}), 404
            
            # Check if the user account is disabled
            if current_user.get("status") == 'disabled':
                return jsonify({'error': 'Contact your administrator to activate your account!'}), 403

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401
        
        current_user['account_type']=data['account_type']
        
        # Pass the current_user to the decorated function
        return f(current_user, *args, **kwargs)
    
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode the JWT token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            
            # Query Admin table
            AdminCheckQuery = text('SELECT * FROM Admin WHERE Email = :email')
            admin_result =  db.session.execute(AdminCheckQuery, {"email": data["email"]}).mappings().first()
            if not admin_result:
                return jsonify({'error': 'Unauthorized access!'}), 403
            
            admin_result = dict(admin_result)
            # Check if the user is an admin with Admin_Type=1
            if admin_result.get("Admin_Type") !="admin" :
                return jsonify({'error': 'Access restricted to admins only!'}), 403
            
            # Pass the admin details to the decorated function
            return f(admin_result, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401
    
    return decorated

def register_validator_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode the JWT token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            
            # Query Admin table
            AdminCheckQuery = text('SELECT * FROM Admin WHERE Email = :email')
            admin_result = db.session.execute(AdminCheckQuery, {"email": data["email"]}).mappings().first()
            if not admin_result:
                return jsonify({'error': 'Unauthorized access!'}), 403
            
            admin_result = dict(admin_result)
            
            # Check if the user is a register validator with Admin_Type=2
            if admin_result.get("Admin_Type") != "registerValidator":
                return jsonify({'error': 'Access restricted to register validators only!'}), 403
            
            # Pass the admin details to the decorated function
            return f(admin_result, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401
    
    return decorated


def etudiant_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode the JWT token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            
            # Query Etudiant table
            EtudiantCheckQuery = text('SELECT * FROM Etudiant WHERE Email = :email')
            etudiant_result = db.session.execute(EtudiantCheckQuery, {"email": data["email"]}).mappings().first()
            if not etudiant_result:
                return jsonify({'error': 'Unauthorized access!'}), 403
            
            etudiant_result = dict(etudiant_result)
            
            # Pass the etudiant details to the decorated function
            return f(etudiant_result, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401
    
    return decorated


def annonceur_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode the JWT token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            
            # Query Annonceur table
            AnnonceurCheckQuery = text('SELECT * FROM Annonceur WHERE Email = :email')
            annonceur_result = db.session.execute(AnnonceurCheckQuery, {"email": data["email"]}).mappings().first()
            if not annonceur_result:
                return jsonify({'error': 'Unauthorized access!'}), 403
            

            annonceur_result = dict(annonceur_result)
            
            # Pass the annonceur details to the decorated function
            return f(annonceur_result, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401
    
    return decorated


def annonceur_or_admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get the token from the Authorization header
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode the JWT token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            
            # Initialize variables
            current_user = None
            user_type = None
            
            # check Admin table
            AdminCheckQuery = text('SELECT * FROM Admin WHERE Email = :email')
            admin_result = db.session.execute(AdminCheckQuery, {"email": data["email"]}).mappings().first()
            if admin_result:
                 current_user =dict(admin_result)
                   
            
            # If not found in Admin, check Annonceur table
            if not current_user:
                AnnonceurCheckQuery = text('SELECT * FROM Annonceur WHERE Email = :email')
                annonceur_result = db.session.execute(AnnonceurCheckQuery, {"email": data["email"]}).mappings().first()
                if annonceur_result:
                    current_user =dict(annonceur_result)
            
            # If no user is found, return an error
            if not current_user:
                return jsonify({'error': 'User not found!'}), 404
            
            # Check if the user account is disabled
            if current_user.get("status") == 'disabled':
                return jsonify({'error': 'Contact your administrator to activate your account!'}), 403

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401
        
        current_user['account_type']=data['account_type']
        
        # Pass the current_user to the decorated function
        return f(current_user, *args, **kwargs)
    
    return decorated