from flask import Blueprint,jsonify,send_from_directory,current_app
import os



accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/file/<filename>', methods=['GET'])
def get_profile_image(filename):
    try:
        # Ensure filename is safe and properly sanitized
        safe_filename = os.path.basename(filename)

        # Construct the path to the directory where profiles are stored
        email = filename.split('_')[0]
        print("\n\n the email",email,"\n\n")
        profile_directory = os.path.abspath(os.path.join(   
            current_app.root_path,'..' ,'data','profiles', email))

        # Check if file exists
        file_path = os.path.join(profile_directory, safe_filename)
        print("the file path: ",file_path)
        if not os.path.exists(file_path):
            return jsonify({'error': 'fichier introuvable'}), 404

        # Serve the file from the specified directory
        return send_from_directory(profile_directory, safe_filename)
    except Exception as e:
        return jsonify({'error': "Fichier de diffusion d'erreurs.", 'details': str(e)}), 500
