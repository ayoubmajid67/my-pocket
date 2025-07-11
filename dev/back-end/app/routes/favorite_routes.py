
from flask import Blueprint,jsonify
from flask import request
import app.utils.utile as Utile
from sqlalchemy import text 
from datetime import datetime
from app.db import db
from app.routes.decorators.authDecorators import token_required
favorite_bp = Blueprint('favorite', __name__)

@favorite_bp.route('/<offer_id>', methods=['POST'])
@token_required
def add_offer_to_favorites(user,offer_id):
    try:
        # Validate input fields
        data = request.get_json() or {}
        required_fields = {'Type'}
        # Check if all required fields are present
        is_valid, missing_fields =Utile.validate_input(data, required_fields)
        if not is_valid:
            return jsonify({'error': 'Missing fields', 'missing_fields': list(missing_fields)}), 400
        type = data['Type'].strip()

        # Authenticate user by checking all relevant tables
        offer_types = ['Produit', 'Logement', 'OffreEmploi']
        if type not in offer_types:
        # Handle the case where 'type' is not a valid offer type
            return jsonify({'Invalid offer type: ': type}),401
        
        #check offer existence 
        check_query = text(f"SELECT * FROM {type} WHERE {type}Id = :offerId")
        result = db.session.execute(check_query, {'offerId': offer_id})
        offer = result.fetchone()
        if not offer:
            return jsonify({'Offer with id not found':offer_id}),404
        
        # Prepare data for insertion
        FK_AdminId = None
        FK_AnnonceurId = None
        EtudiantId = None

        if user['account_type'] == 'Admin':
            FK_AdminId = user['AdminId']
        elif user['account_type'] == 'Annonceur':
            FK_AnnonceurId = user['AnnonceurId']
        else:
            EtudiantId = user['EtudiantId']

        ProduitId = offer_id if type == 'Produit' else None
        LogementId = offer_id if type == 'Logement' else None
        OffreEmploiId = offer_id if type == 'OffreEmploi' else None
        print ('fdlilkmgnmdlkdfn',FK_AdminId, FK_AnnonceurId, EtudiantId, ProduitId, LogementId, OffreEmploiId)
        #check offer existence in favorites list
        check_query = text("""SELECT * FROM favorites WHERE 
            (Fk_AdminId = :FK_AdminId OR (Fk_AdminId IS NULL AND :FK_AdminId IS NULL))
            AND (Fk_AnnonceurId = :FK_AnnonceurId OR (Fk_AnnonceurId IS NULL AND :FK_AnnonceurId IS NULL))
            AND (Fk_EtudiantId = :FK_EtudiantId OR (Fk_EtudiantId IS NULL AND :FK_EtudiantId IS NULL))
            AND (ProduitId = :ProduitId OR (ProduitId IS NULL AND :ProduitId IS NULL))
            AND (LogementId = :LogementId OR (LogementId IS NULL AND :LogementId IS NULL))
            AND (OffreEmploiId = :OffreEmploiId OR (OffreEmploiId IS NULL AND :OffreEmploiId IS NULL))
        """)
        result = db.session.execute(check_query, {'FK_AdminId': FK_AdminId, 'FK_AnnonceurId': FK_AnnonceurId, 'FK_EtudiantId': EtudiantId, 'ProduitId': ProduitId, 'LogementId': LogementId, 'OffreEmploiId': OffreEmploiId})
        offer = result.fetchall()
        print('offer',offer)
        if offer:
            return jsonify({'Offer already exist in favorites id':offer_id}),404
        
        # Insert into Favoris table
        insert_query = text("""
        INSERT INTO favorites (DateAjout, FK_AdminId, FK_AnnonceurId, FK_EtudiantId, ProduitId, LogementId, OffreEmploiId, Type)
        VALUES (:DateAjout, :FK_AdminId, :FK_AnnonceurId, :FK_EtudiantId, :ProduitId, :LogementId, :OffreEmploiId, :type)
        """)
        db.session.execute(insert_query, {
            'DateAjout': datetime.now(),
            'FK_AdminId': FK_AdminId,
            'FK_AnnonceurId': FK_AnnonceurId,
            'FK_EtudiantId': EtudiantId,
            'ProduitId': ProduitId,
            'LogementId': LogementId,
            'OffreEmploiId': OffreEmploiId,
            'type': type
        })
        db.session.commit()  # Commit the transaction

        return jsonify({'message': 'Offer added to favorites'}), 201
    except Exception as e:
        return jsonify({'Global error': str(e)}), 500

@favorite_bp.route('/<favorite_id>', methods=['DELETE'])
@token_required
def delete_offer_from_favorites(user, favorite_id):
    try:
        # Prepare data for deletion
        FK_AdminId = None
        FK_AnnonceurId = None
        EtudiantId = None

        if user['account_type'] == 'Admin':
            FK_AdminId = user['AdminId']
        elif user['account_type'] == 'Annonceur':
            FK_AnnonceurId = user['AnnonceurId']
        else:
            EtudiantId = user['EtudiantId']

        print('User:', user)
        print('Data:', FK_AdminId, FK_AnnonceurId, EtudiantId, favorite_id)

        # Delete the favorite
        delete_query = text("""
        DELETE FROM favorites 
        WHERE FavoriId = :FavoriId 
          AND (Fk_AdminId = :FK_AdminId OR (Fk_AdminId IS NULL AND :FK_AdminId IS NULL))
          AND (Fk_AnnonceurId = :FK_AnnonceurId OR (Fk_AnnonceurId IS NULL AND :FK_AnnonceurId IS NULL))
          AND (Fk_EtudiantId = :FK_EtudiantId OR (Fk_EtudiantId IS NULL AND :FK_EtudiantId IS NULL))
        """)
        result = db.session.execute(delete_query, {
            'FavoriId': favorite_id,
            'FK_AdminId': FK_AdminId,
            'FK_AnnonceurId': FK_AnnonceurId,
            'FK_EtudiantId': EtudiantId
        })
        db.session.commit()

        # Check if any rows were deleted
        if result.rowcount == 0:
            return jsonify({'error': 'Favorite not found or you do not have permission to delete it'}), 404

        return jsonify({'message': 'Offer deleted successfully from favorites'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'Global error': str(e)}), 500

@favorite_bp.route('', methods=['GET'])
@token_required
def get_favorites(user):
    try:
        # Prepare data for get
        FK_AdminId = None
        FK_AnnonceurId = None
        EtudiantId = None

        if user['account_type'] == 'Admin':
            FK_AdminId = user['AdminId']
        elif user['account_type'] == 'Annonceur':
            FK_AnnonceurId = user['AnnonceurId']
        else:
            EtudiantId = user['EtudiantId']

        # Get all favorites
        getFavoritesQuery = text("""
        SELECT * FROM favorites WHERE FK_AdminId = :FK_AdminId OR FK_AnnonceurId = :FK_AnnonceurId OR FK_EtudiantId = :FK_EtudiantId
        """)
        result = db.session.execute(getFavoritesQuery, {'FK_AdminId': FK_AdminId, 'FK_AnnonceurId': FK_AnnonceurId, 'FK_EtudiantId': EtudiantId})
        favorites = result.fetchall()
        # Convert rows to dictionaries
        favorites_list = []
        for favorite in favorites:
            favorites_list.append({
                'FavoriId': favorite.FavoriId,  # Replace with actual column names
                'DateAjout': favorite.DateAjout,
                'FK_AdminId': favorite.FK_AdminId,
                'FK_AnnonceurId': favorite.FK_AnnonceurId,
                'FK_EtudiantId': favorite.FK_EtudiantId,
                'ProduitId': favorite.ProduitId,
                'LogementId': favorite.LogementId,
                'OffreEmploiId': favorite.OffreEmploiId,
                'Type': favorite.Type
            })

        return jsonify(favorites_list), 200    
    except Exception as e:
        return jsonify({'Global error': str(e)}), 500
