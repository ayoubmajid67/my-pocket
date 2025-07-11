from flask import Blueprint,send_from_directory
from app.routes.decorators.authDecorators import *
import app.utils.utile as Utile
from PIL import Image
import shutil

productsOffer_bp = Blueprint('productsOffer', __name__)


def is_annonceur_owner_of_product(annonceur_id, product_id):
    query = text("SELECT FK_AnnonceurId FROM Produit WHERE ProduitId = :product_id")
    result = db.session.execute(query, {"product_id": product_id}).scalar()
    return result == annonceur_id




@productsOffer_bp.route('', methods=['GET'])
def get_products_offers():
    # Fetch all products from the database
    query = text("SELECT * FROM Produit")
    results = db.session.execute(query).mappings().all()

    # Convert RowMapping objects to dictionaries
    products = [dict(result) for result in results]

    # Get server IP and port
    server_ip, server_port = Utile.get_request_server_port(request)

    # Generate URLs for product images
    for product in products:
        product_id = product['ProduitId']
        image_query = text("SELECT ImageId FROM ProduitImages WHERE FK_ProduitId = :product_id")
        image_results = db.session.execute(image_query, {"product_id": product_id}).scalars().all()
        
        product['images'] = [
            Utile.get_product_img_url(server_ip, server_port, f"image_{image_id}.webp", product_id)
            for image_id in image_results
        ]

    return jsonify(products), 200

@productsOffer_bp.route('/<int:productOffer_id>', methods=['GET'])
def get_product_offer(productOffer_id):
    # Fetch a specific product by ID
    query = text("SELECT * FROM Produit WHERE ProduitId = :product_id")
    result = db.session.execute(query, {"product_id": productOffer_id}).mappings().first()

    if not result:
        return jsonify({'error': 'Product not found'}), 404

    product = dict(result)

    # Get server IP and port
    server_ip, server_port = Utile.get_request_server_port(request)

    # Generate URLs for product images
    image_query = text("SELECT ImageId FROM ProduitImages WHERE FK_ProduitId = :product_id")
    image_results = db.session.execute(image_query, {"product_id": productOffer_id}).scalars().all()
    
    product['images'] = [
        Utile.get_product_img_url(server_ip, server_port, f"image_{image_id}.webp", productOffer_id)
        for image_id in image_results
    ]

    return jsonify(product), 200

import os

@productsOffer_bp.route('/<int:product_id>/file/<filename>', methods=['GET'])
def get_product_offer_image(product_id,filename):
            # Ensure filename is safe and properly sanitized
    try :        
        safe_filename = os.path.basename(filename)


        product_directory = os.path.abspath(os.path.join(   
            current_app.root_path,'..' ,'data','products', str(product_id)))

        # Check if file exists
        file_path = os.path.join(product_directory, safe_filename)

        print("\n\n the file path ",file_path,"\n\n")
   
        if not os.path.exists(file_path):
            return jsonify({'error': 'fichier introuvable'}), 404

        # Serve the file from the specified directory
        return send_from_directory(product_directory, safe_filename)
    except Exception as e:
        return jsonify({'error': "Fichier de diffusion d'erreurs.", 'details': str(e)}), 500

  
@productsOffer_bp.route('', methods=['POST'])
@annonceur_required
def add_product_offer(annonceur):
    data = request.form.to_dict()
    files = request.files

    required_fields = ['Categorie', 'Description', 'Disponible', 'Nom', 'Prix', 'Stock']
    is_valid, missing_fields = Utile.validate_input(data, required_fields)
    
    if not is_valid:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    # Validate numeric fields
    try:
        prix = float(data['Prix'])
        stock = int(data['Stock'])
        disponible = int(data['Disponible'])
    except ValueError:
        return jsonify({'error': 'Prix, Stock, and Disponible must be valid numbers'}), 400
    
    if stock < 0 or prix < 0 :
         return jsonify({'error': 'Prix, Stock, should be positive'}), 400


    # Validate that Disponible is 0 or 1
    if disponible not in (0, 1):
        return jsonify({'error': 'Disponible must be 0 or 1'}), 400

    # Check for existing product with the same name
    check_nom_query = text("SELECT Nom FROM Produit WHERE Nom = :nom")
    existing_product = db.session.execute(check_nom_query, {"nom": data['Nom']}).scalar()
    if existing_product:
        return jsonify({'error': 'Product name already exists'}), 409

    # Validate images
    if 'images' not in files or len(files.getlist('images')) < 1:
        return jsonify({'error': 'At least one image must be provided'}), 400

    # Validate image extensions
    allowed_extensions = current_app.config['ALLOWED_IMG_EXTENSIONS']
    for image_file in files.getlist('images'):
        _, ext = os.path.splitext(image_file.filename)
        if ext.lower().lstrip('.') not in allowed_extensions:
            return jsonify({'error': f'Invalid image format {ext}. Allowed formats: {", ".join(allowed_extensions)}'}), 400

    # Process product data
    categorie = data['Categorie'].strip()
    description = data['Description'].strip()
    nom = data['Nom'].strip()
    annonceur_id = annonceur['AnnonceurId']

    # Insert into Produit table
    insert_query = text("""
        INSERT INTO Produit (
            Categorie, Description, Disponible, FK_AnnonceurId, Nom, Prix, Stock
        ) VALUES (
            :categorie, :description, :disponible, :annonceur_id, :nom, :prix, :stock
        )
    """)
    db.session.execute(insert_query, {
        "categorie": categorie,
        "description": description,
        "disponible": disponible,
        "annonceur_id": annonceur_id,
        "nom": nom,
        "prix": prix,
        "stock": stock
    })
    db.session.commit()

    product_id = db.session.execute(text("SELECT LAST_INSERT_ID()")).scalar()

    # Create directory for product images
    product_dir = os.path.join("data", "products", str(product_id))
    os.makedirs(product_dir, exist_ok=True)

    # Process images and save as WebP
    image_id = 1
    for image_file in files.getlist('images'):
        # Validate and convert image
        try:
            img = Image.open(image_file.stream)
            webp_filename = f"image_{image_id}.webp"
            image_path = os.path.join(product_dir, webp_filename)
            
            # Convert to WebP
            img.save(image_path, 'WEBP', quality=85)
            
            # Insert into ProduitImages
            image_insert_query = text("""
                INSERT INTO ProduitImages (FK_ProduitId, ImageId) VALUES (:product_id, :image_id)
            """)
            db.session.execute(image_insert_query, {
                "product_id": product_id,
                "image_id": image_id
            })
            db.session.commit()
            image_id += 1
        except Exception as e:
            return jsonify({'error': f'Image processing failed: {str(e)}'}), 400

    return jsonify({"message": "Product added successfully", "product_id": product_id}), 201


@productsOffer_bp.route('/<int:productOffer_id>', methods=['PATCH'])
@annonceur_required
def update_product_offer(annonceur, productOffer_id):
    data = request.form.to_dict() if request.form else {}
    files = request.files

    # Define allowed fields for product updates
    allowed_fields = ['Categorie', 'Description', 'Disponible', 'Nom', 'Prix', 'Stock']

    # Check for invalid fields
    invalid_fields = [field for field in data if field not in allowed_fields]
    existed_fields = [field for field in data if field in allowed_fields and data[field].strip()!=""]

  
    if invalid_fields:
        return jsonify({'error': f'Invalid fields provided: {", ".join(invalid_fields)}'}), 400
    
    if len(existed_fields)==0:
        return jsonify({'error': f'you have to proved at least one field to update'}), 400

    # Check product existence and ownership
    product_query = text("SELECT * FROM Produit WHERE ProduitId = :product_id")
    product = db.session.execute(product_query, {"product_id": productOffer_id}).mappings().first()
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    product = dict(product)

    if not is_annonceur_owner_of_product(annonceur['AnnonceurId'], productOffer_id):
        return jsonify({'error': 'Unauthorized to update this product'}), 403

    # Prepare update parameters with existing values as defaults
    update_params = {
        "categorie": product['Categorie'],
        "description": product['Description'],
        "disponible": product['Disponible'],
        "nom": product['Nom'],
        "prix": product['Prix'],
        "stock": product['Stock'],
        "product_id": productOffer_id
    }

    # Validate and update provided fields
    for field in data:
        if field == 'Disponible':
            try:
                disponible = int(data[field])
                if disponible not in (0, 1):
                    raise ValueError
                update_params[field] = disponible
            except ValueError:
                return jsonify({'error': 'Disponible must be 0 or 1'}), 400
        elif field == 'Prix':
            try:
                prix = float(data[field])
                if   prix <= 0 :
                        return jsonify({'error': 'Prix, should be positive'}), 400
                update_params[field] = prix
            except ValueError:
                return jsonify({'error': 'Prix must be a valid number'}), 400
        elif field == 'Stock':
            try:
                stock = int(data[field])
                if   stock <= 0 :
                        return jsonify({'error': 'Stock, should be positive'}), 400
                update_params[field] = stock
            except ValueError:
                return jsonify({'error': 'Stock must be a valid integer'}), 400
        else:
            # For string fields (Categorie, Description, Nom)
            update_params[field] = data[field].strip() if data[field] else product[field]

    # Check if the new product name already exists
    if 'Nom' in data:
        new_nom = data['Nom'].strip()
        if new_nom != product['Nom']:
            check_nom_query = text("SELECT Nom FROM Produit WHERE Nom = :new_nom AND ProduitId != :product_id")
            existing_product = db.session.execute(check_nom_query, {"new_nom": new_nom, "product_id": productOffer_id}).scalar()
            if existing_product:
                return jsonify({'error': 'Product name already exists'}), 409

    # Update only provided fields
    set_clause = ', '.join([f"{col} = :{col}" for col in    data.keys()])
    update_query = text(f"""
        UPDATE Produit 
        SET {set_clause}
        WHERE ProduitId = :product_id
    """)

    print("the update query",update_query)


    try:
        db.session.execute(update_query, update_params)
        db.session.commit()
    except Exception as e:
        return jsonify({'error': f'Database update failed: {str(e)}'}), 400

    # Handle images (optional)
    if 'images' in files:
        # Validate image extensions
        allowed_extensions = current_app.config['ALLOWED_IMG_EXTENSIONS']
        for image_file in files.getlist('images'):
            _, ext = os.path.splitext(image_file.filename)
            if ext.lower().lstrip('.') not in allowed_extensions:
                return jsonify({'error': f'Invalid image format {ext}'}), 400

        # Delete existing images
        delete_images_query = text("DELETE FROM ProduitImages WHERE FK_ProduitId = :product_id")
        db.session.execute(delete_images_query, {"product_id": productOffer_id})
        db.session.commit()

        # Save new images
        product_dir = os.path.join("data", "products", str(productOffer_id))
        os.makedirs(product_dir, exist_ok=True)

        image_id = 1
        for image_file in files.getlist('images'):
            try:
                img = Image.open(image_file.stream)
                image_path = os.path.join(product_dir, f"image_{image_id}.webp")
                img.save(image_path, 'WEBP', quality=85)

                # Insert into ProduitImages
                image_insert_query = text("""
                    INSERT INTO ProduitImages (FK_ProduitId, ImageId) 
                    VALUES (:product_id, :image_id)
                """)
                db.session.execute(image_insert_query, {
                    "product_id": productOffer_id,
                    "image_id": image_id
                })
                db.session.commit()
                image_id += 1
            except Exception as e:
                return jsonify({'error': f'Image processing failed: {str(e)}'}), 400

    return jsonify({
        "message": "Product updated successfully",
        "updated_fields": list(data.keys()),
        "product_id": productOffer_id
    }), 200
@productsOffer_bp.route('/<int:productOffer_id>', methods=['DELETE'])
@annonceur_or_admin_required
def delete_product_offer(user, productOffer_id):
    # Check product existence
    product_query = text("SELECT * FROM Produit WHERE ProduitId = :product_id")
    product = db.session.execute(product_query, {"product_id": productOffer_id}).mappings().first()
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    product = dict(product)

    # Check permissions
    if user['account_type'] != 'Admin' and not is_annonceur_owner_of_product(user['AnnonceurId'], productOffer_id):
            return jsonify({'error': 'Unauthorized to delete this product'}), 403

    # Delete product images from filesystem
    product_dir = os.path.join("data", "products", str(productOffer_id))
    if os.path.exists(product_dir):
        shutil.rmtree(product_dir)

    # Delete database records
    delete_query = text("DELETE FROM Produit WHERE ProduitId = :product_id")
    db.session.execute(delete_query, {"product_id": productOffer_id})
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200

