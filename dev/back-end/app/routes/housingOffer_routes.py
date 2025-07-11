from flask import Blueprint, jsonify, request, current_app,send_from_directory
from sqlalchemy import text
from app.routes.decorators.authDecorators import *
from app.db import db
import os
from PIL import Image
import shutil
import app.utils.utile as Utile

housingOffer_bp = Blueprint('housingOffer', __name__)

def is_annonceur_owner_of_logement(annonceur_id, housing_id):
    query = text("SELECT FK_AnnonceurId FROM Logement WHERE LogementId = :housing_id")
    result = db.session.execute(query, {"housing_id": housing_id}).scalar()
    return result == annonceur_id

@housingOffer_bp.route('', methods=['POST'])
@annonceur_required
def add_housing_offer(annonceur):
    data = request.form.to_dict()
    files = request.files

    required_fields = ['Titre', 'Localisation', 'Prix', 'Status','XPosition','YPosition']
    is_valid, missing_fields = Utile.validate_input(data, required_fields)
    if not is_valid:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    # Validate Status
    allowed_status = ['Disponible', 'Réservé', 'Indisponible']
    if data['Status'] not in allowed_status:
        return jsonify({'error': 'Invalid Status value. Must be Disponible/Réservé/Indisponible'}), 400

    # Check duplicate Titre
    check_nom_query = text("SELECT Titre FROM Logement WHERE Titre = :titre")
    existing_housing = db.session.execute(check_nom_query, {"titre": data['Titre']}).scalar()
    if existing_housing:
        return jsonify({'error': 'Housing title already exists'}), 409

    # Validate images
    if 'images' not in files or len(files.getlist('images')) < 1:
        return jsonify({'error': 'At least one image must be provided'}), 400

    allowed_extensions = current_app.config['ALLOWED_IMG_EXTENSIONS']
    for image_file in files.getlist('images'):
        _, ext = os.path.splitext(image_file.filename)
        if ext.lower().lstrip('.') not in allowed_extensions:
            return jsonify({'error': f'Invalid image format {ext}'}), 400

    # Process data
    titre = data['Titre'].strip()
    localisation = data['Localisation'].strip()
    try : 
        prix = float(data['Prix'])
        if   prix <= 0 :
                        return jsonify({'error': 'Prix, should be positive'}), 400
    except ValueError :
         return jsonify({"error":"Prix must be a valid number"}),400
    

    try : 
        xPosition = float(data['XPosition'])
        
    except ValueError :
         return jsonify({"error":"xPosition must be a valid number"}),400
    
    try : 
        yPosition = float(data['YPosition'])
        
    except ValueError :
         return jsonify({"error":"YPosition must be a valid number"}),400
    
    
    status = data['Status']
    description = data.get('Description', '').strip()

    annonceur_id = annonceur['AnnonceurId']

    # Insert into Logement table
    insert_query = text("""
        INSERT INTO Logement (
            Titre, Localisation, Prix, Status,XPosition,YPosition, FK_AnnonceurId, Description
        ) VALUES (
            :titre, :localisation, :prix,:Status ,:xPosition,:yPosition,:annonceur_id,:description
        )
    """)
    db.session.execute(insert_query, {
        "titre": titre,
        "localisation": localisation,
        "prix": prix,
        "Status": status,
        "xPosition":xPosition,
        "yPosition":yPosition,
        "annonceur_id": annonceur_id,
        "description": description
    })
    db.session.commit()
    
    housing_id = db.session.execute(text("SELECT LAST_INSERT_ID()")).scalar()

    # Create directory for housing images
    housing_dir = os.path.join("data", "housing", str(housing_id))
    os.makedirs(housing_dir, exist_ok=True)

    image_id = 1
    for image_file in files.getlist('images'):
        try:
            img = Image.open(image_file.stream)
            webp_filename = f"image_{image_id}.webp"
            image_path = os.path.join(housing_dir, webp_filename)
            img.save(image_path, 'WEBP', quality=85)

            # Insert into LogementImages
            image_insert_query = text("""
                INSERT INTO LogementImages (FK_LogementId, ImageId) 
                VALUES (:housing_id, :image_id)
            """)
            db.session.execute(image_insert_query, {
                "housing_id": housing_id,
                "image_id": image_id
            })
            db.session.commit()
            image_id += 1
        except Exception as e:
            return jsonify({'error': f'Image processing failed: {str(e)}'}), 400

    return jsonify({
        "message": "Housing offer added successfully",
        "housing_id": housing_id
    }), 201


@housingOffer_bp.route('/<int:housingOffer_id>', methods=['PATCH'])
@annonceur_required
def update_housing_offer(annonceur, housingOffer_id):
    data = request.form.to_dict() or {}
    files = request.files

    # Allowed fields
    allowed_fields = ['Titre', 'Localisation', 'Prix', 'Status', 'Description','XPosition','YPosition']
    
    # Validate fields
    invalid_fields = [field for field in data if field not in allowed_fields]
    existed_fields = [field for field in data if field in allowed_fields and data[field].strip()!=""]
    if invalid_fields:
        return jsonify({'error': f'Invalid fields: {", ".join(invalid_fields)}'}), 400
    
    
    if len(existed_fields)==0:
        return jsonify({'error': f'you have to proved at least one field to update'}), 400

    # Check existence and ownership
    housing_query = text("SELECT * FROM Logement WHERE LogementId = :housing_id")
    housing = db.session.execute(housing_query, {"housing_id": housingOffer_id}).mappings().first()
    if not housing:
        return jsonify({'error': 'Housing offer not found'}), 404
    housing = dict(housing)
    
    if not is_annonceur_owner_of_logement(annonceur['AnnonceurId'], housingOffer_id):
        return jsonify({'error': 'Unauthorized to update this housing offer'}), 403

    # Prepare update parameters
    update_params = {
        "titre": housing['Titre'],
        "localisation": housing['Localisation'],
        "prix": housing['Prix'],
        "Status": housing['Status'],
        "description": housing['Description'],
        "housing_id": housingOffer_id,
        "xPosition":housing["XPosition"],
        "yPosition":housing["YPosition"]
    }

    # Validate and update provided fields
    for field in data:
        if field == 'Prix':
            try:
                prix = float(data[field])
                if prix <= 0:
                    raise ValueError
                update_params[field] = prix
            except ValueError:
                return jsonify({'error': 'Prix must be a positive number'}), 400
        if field=="XPosition" :
            try:
                xPosition = float(data[field])
                
                update_params[field] = xPosition
            except ValueError:
                return jsonify({'error': 'XPosition must be a number'}), 400
            
        if field=="YPosition" :
            try:
                yPosition = float(data[field])
                
                update_params[field] = yPosition
            except ValueError:
                return jsonify({'error': 'YPosition must be a number'}), 400
        
        elif field == 'Status':
            if data[field] not in ['Disponible', 'Réservé', 'Indisponible']:
                return jsonify({'error': 'Invalid Status value'}), 400
            update_params[field] = data[field]
        else:
            update_params[field] = data[field].strip() if data[field] else housing.get(field)

        # Check for duplicate Titre
        if field == 'Titre':
            new_titre = data[field].strip()
            if new_titre != housing['Titre']:
                check_titre = text("SELECT Titre FROM Logement WHERE Titre = :titre AND LogementId != :id")
                existing = db.session.execute(check_titre, {"titre": new_titre, "id": housingOffer_id}).scalar()
                if existing:
                    return jsonify({'error': 'Housing title already exists'}), 409

    # Build dynamic SQL update
    set_clause = ', '.join([f"{col} = :{col}" for col in data.keys()])
    update_query = text(f"""
        UPDATE Logement 
        SET {set_clause}
        WHERE LogementId = :housing_id
    """)
    
    try:
        db.session.execute(update_query, update_params)
        db.session.commit()
    except Exception as e:
        return jsonify({'error': f'Database update failed: {str(e)}'}), 400

    # Handle images
    if 'images' in files:
        # Delete old images
        delete_images = text("DELETE FROM LogementImages WHERE FK_LogementId = :housing_id")
        db.session.execute(delete_images, {"housing_id": housingOffer_id})
        db.session.commit()
        
        # Save new images
        housing_dir = os.path.join("data", "housing", str(housingOffer_id))
        os.makedirs(housing_dir, exist_ok=True)
        image_id = 1
        for image_file in files.getlist('images'):
            try:
                img = Image.open(image_file.stream)
                webp_filename = f"image_{image_id}.webp"
                image_path = os.path.join(housing_dir, webp_filename)
                img.save(image_path, 'WEBP', quality=85)

                # Insert into LogementImages
                image_insert_query = text("""
                    INSERT INTO LogementImages (FK_LogementId, ImageId) 
                    VALUES (:housing_id, :image_id)
                """)
                db.session.execute(image_insert_query, {
                    "housing_id": housingOffer_id,
                    "image_id": image_id
                })
                db.session.commit()
                image_id += 1
            except Exception as e:
                return jsonify({'error': f'Image processing failed: {str(e)}'}), 400

    return jsonify({
        "message": "Housing offer updated successfully",
        "updated_fields": list(data.keys()),
        "housing_id": housingOffer_id
    }), 200


@housingOffer_bp.route('/<int:housingOffer_id>', methods=['DELETE'])
@annonceur_or_admin_required
def delete_housing_offer(user, housingOffer_id):
    # Check existence
    housing_query = text("SELECT * FROM Logement WHERE LogementId = :id")
    housing = db.session.execute(housing_query, {"id": housingOffer_id}).mappings().first()
    if not housing:
        return jsonify({'error': 'Housing offer not found'}), 404
    
    # Check permissions
    if user['account_type'] == 'Annonceur':
        if not is_annonceur_owner_of_logement(user['AnnonceurId'], housingOffer_id):
            return jsonify({'error': 'Unauthorized to delete this housing offer'}), 403
    elif user['account_type'] != 'Admin':
        return jsonify({'error': 'Unauthorized access'}), 403

    # Delete images from filesystem
    housing_dir = os.path.join("data", "housing", str(housingOffer_id))
    if os.path.exists(housing_dir):
        shutil.rmtree(housing_dir)

    # Delete database records
    delete_query = text("DELETE FROM Logement WHERE LogementId = :id")
    db.session.execute(delete_query, {"id": housingOffer_id})
    db.session.commit()

    return jsonify({"message": "Housing offer deleted successfully"}), 200


@housingOffer_bp.route('/<int:housingOffer_id>', methods=['GET'])
def get_housing_offer(housingOffer_id):
    query = text("SELECT * FROM Logement WHERE LogementId = :id")
    result = db.session.execute(query, {"id": housingOffer_id}).mappings().first()
    if not result:
        return jsonify({'error': 'Housing offer not found'}), 404
    housing = dict(result)
    
    server_ip, server_port = Utile.get_request_server_port(request)
    
    # Get images
    image_query = text("SELECT ImageId FROM LogementImages WHERE FK_LogementId = :id")
    image_results = db.session.execute(image_query, {"id": housingOffer_id}).scalars().all()
    housing['images'] = [
        Utile.get_housing_offer_img_url(server_ip, server_port, f"image_{image_id}.webp", housingOffer_id)
        for image_id in image_results
    ]

    return jsonify(housing), 200


@housingOffer_bp.route('', methods=['GET'])
def get_housing_offers():
    query = text("SELECT * FROM Logement")
    results = db.session.execute(query).mappings().all()
    housings = [dict(housing) for housing in results]
    
    server_ip, server_port = Utile.get_request_server_port(request)
    
    for housing in housings:
        housing_id = housing['LogementId']
        image_query = text("SELECT ImageId FROM LogementImages WHERE FK_LogementId = :id")
        images = db.session.execute(image_query, {"id": housing_id}).scalars().all()
        housing['images'] = [
            Utile.get_housing_offer_img_url(server_ip, server_port, f"image_{img_id}.webp", housing_id)
            for img_id in images
        ]

    return jsonify(housings), 200


@housingOffer_bp.route('/<int:housing_id>/file/<filename>', methods=['GET'])
def get_housing_offer_image(housing_id, filename):
    try:
        safe_filename = os.path.basename(filename)
        housing_dir = os.path.abspath(os.path.join(
            current_app.root_path, '..', 'data', 'housing', str(housing_id)
        ))
        file_path = os.path.join(housing_dir, safe_filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        return send_from_directory(housing_dir, safe_filename)
    except Exception as e:
        return jsonify({'error': f'Error serving file: {str(e)}'}), 500
    
@housingOffer_bp.route('/<housing_id>/apply', methods=['POST'])
@etudiant_required
def apply_for_a_housing_offer(etudiant, housing_id):
    