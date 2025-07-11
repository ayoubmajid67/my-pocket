from flask import Blueprint,jsonify
from flask import request
import app.utils.utile as Utile
from sqlalchemy import text 
from datetime import datetime
from app.db import db
from app.routes.decorators.authDecorators import token_required

from flask import Blueprint

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('', methods=['GET'])
@token_required
def get_orders(user):
    try:
        if user['account_type'] == 'Etudiant':
            # Query to fetch orders and their commandelines
            get_Etudiant_orders = text("""
                SELECT c.*, cl.*
                FROM commande c
                INNER JOIN commandeline cl ON c.CommandeId = cl.PK_CommandeId
                WHERE c.FK_EtudiantId = :EtudiantId
            """)

            result = db.session.execute(get_Etudiant_orders, {'EtudiantId': user['EtudiantId']})
            orders = result.fetchall()

            # Dictionary to group commandelines by CommandeId
            orders_dict = {}

            for order in orders:
                commande_id = order.CommandeId

                # Create a new entry for the commande if it doesn't exist
                if commande_id not in orders_dict:
                    orders_dict[commande_id] = {
                        'CommandeId': order.CommandeId,
                        'DateCommande': order.DateCommande,
                        'FK_EtudiantId': order.FK_EtudiantId,
                        'MontantTotal': order.MontantTotal,
                        'commandelines': []  # List to hold commandelines
                    }

                # Append the current commandeline to the commande's list
                orders_dict[commande_id]['commandelines'].append({
                    'PK_ProduitId': order.PK_ProduitId,
                    'PrixUnitaire': order.PrixUnitaire,
                    'Quantite': order.Quantite,
                })

            # Convert the dictionary values to a list for the final response
            orders_list = list(orders_dict.values())

            return jsonify(orders_list), 200
        elif user['account_type'] == 'Annonceur':
            get_Annonceur_orders = text("""
                SELECT p.*, cl.*, c.*
                FROM produit p
                INNER JOIN commandeline cl ON p.ProduitId = cl.PK_ProduitId
                INNER JOIN commande c ON cl.PK_CommandeId = c.CommandeId
                WHERE p.FK_AnnonceurId = :AnnonceurId
            """)
            result = db.session.execute(get_Annonceur_orders, {'AnnonceurId': user['AnnonceurId']})
            orders = result.fetchall()

            # Dictionary to group commandes by ProduitId
            products_dict = {}
            for order in orders:
                produit_id = order.ProduitId

                # Create a new entry for the product if it doesn't exist
                if produit_id not in products_dict:
                    products_dict[produit_id] = {
                        'ProduitId': order.ProduitId,
                        'Categorie' : order.Categorie,
                        'Description' : order.Description,
                        'Disponible' : order.Disponible,
                        'Nom' : order.Nom,
                        'FK_AnnonceurId': order.FK_AnnonceurId,
                        'Prix': order.PrixUnitaire,
                        'Stock' : order.Stock,
                        'commandes': []  # List to hold commandes
                    }

                # Append the current commande to the product's list
                products_dict[produit_id]['commandes'].append({
                    'PK_ProduitId': order.PK_ProduitId,
                    'CommandeId': order.CommandeId,
                    'PrixUnitaire': order.PrixUnitaire,
                    'Quantite': order.Quantite,
                    'DateCommande': order.DateCommande,
                    'FK_EtudiantId': order.FK_EtudiantId,
                    'MontantTotal': order.PrixUnitaire * order.Quantite,
                })

            # Convert the dictionary values to a list for the final response
            orders_list = list(products_dict.values())

            return jsonify(orders_list), 200
        elif user['account_type'] == 'Admin':
            get_Admin_orders = text("""
                SELECT c.*, cl.*
                FROM commande c
                INNER JOIN commandeline cl ON c.CommandeId = cl.PK_CommandeId
            """)
            result = db.session.execute(get_Admin_orders)
            orders = result.fetchall()

            # Dictionary to group commandelines by CommandeId
            orders_dict = {}

            for order in orders:
                commande_id = order.CommandeId

                # Create a new entry for the commande if it doesn't exist
                if commande_id not in orders_dict:
                    orders_dict[commande_id] = {
                        'CommandeId': order.CommandeId,
                        'DateCommande': order.DateCommande,
                        'FK_EtudiantId': order.FK_EtudiantId,
                        'MontantTotal': order.MontantTotal,
                        'commandelines': []  # List to hold commandelines
                    }

                # Append the current commandeline to the commande's list
                orders_dict[commande_id]['commandelines'].append({
                    'PK_ProduitId': order.PK_ProduitId,
                    'PrixUnitaire': order.PrixUnitaire,
                    'Quantite': order.Quantite,
                })

            # Convert the dictionary values to a list for the final response
            orders_list = list(orders_dict.values())

            return jsonify(orders_list), 200

        # Fallback response for non-Etudiant users or other cases
        return jsonify({'message': 'No orders available for this account type'}), 404

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'Global error': str(e)}), 500
