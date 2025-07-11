from flask import Blueprint,jsonify,request
from app.routes.decorators.authDecorators import etudiant_required
from app.db import db
from sqlalchemy.exc import SQLAlchemyError

shoppingCard_bp = Blueprint('shoppingCard', __name__)

@shoppingCard_bp.route('/<productOffer_id>', methods=['POST'])
@etudiant_required
def add_product_to_shopping_card(etudiant, productOffer_id):
    try:
        # Récupérer le produit à partir de l'ID
        produit = db.session.execute(
            "SELECT * FROM Produit WHERE ProduitId = :product_id",
            {'product_id': productOffer_id}
        ).fetchone()

        # Vérifier si le produit existe
        if not produit:
            return jsonify({"error": "Produit introuvable"}), 404

        # Vérifier la disponibilité du produit
        if produit['Disponible'] == 0 or produit['Stock'] <= 0:
            return jsonify({"error": "Produit non disponible"}), 400

        # Récupérer la quantité depuis la requête, par défaut 1 si non précisé
        quantite = int(request.json.get('quantite', 1))

        # Vérifier si la quantité demandée est valide
        if quantite <= 0:
            return jsonify({"error": "Quantité invalide"}), 400
        if quantite > produit['Stock']:
            return jsonify({"error": "Quantité demandée supérieure au stock disponible"}), 400

        # Vérifier si l'étudiant a déjà un panier
        panier = db.session.execute(
            "SELECT * FROM Panier WHERE FK_EtudiantId = :etudiant_id",
            {'etudiant_id': etudiant['id']}
        ).fetchone()

        if not panier:
            # Si l'étudiant n'a pas de panier, créer un nouveau panier
            db.session.execute(
                "INSERT INTO Panier (FK_EtudiantId) VALUES (:etudiant_id)",
                {'etudiant_id': etudiant['id']}
            )
            # Récupérer l'ID du panier récemment créé
            panier_id = db.session.execute(
                "SELECT LAST_INSERT_ID()"
            ).fetchone()[0]
        else:
            # Utiliser l'ID du panier existant
            panier_id = panier['PanierId']

        # Vérifier si le produit existe déjà dans le panier
        existing_item = db.session.execute(
            "SELECT * FROM PanierItem WHERE PK_PanierId = :panier_id AND PK_ProduitId = :produit_id",
            {'panier_id': panier_id, 'produit_id': produit['ProduitId']}
        ).fetchone()

        if existing_item:
            # Si l'élément existe déjà, mettre à jour la quantité
            new_quantite = existing_item['Quantite'] + quantite
            db.session.execute(
                "UPDATE PanierItem SET Quantite = :quantite WHERE PK_PanierId = :panier_id AND PK_ProduitId = :produit_id",
                {'quantite': new_quantite, 'panier_id': panier_id, 'produit_id': produit['ProduitId']}
            )
        else:
            # Sinon, ajouter un nouvel article dans le panier
            db.session.execute(
                "INSERT INTO PanierItem (PK_PanierId, PK_ProduitId, Quantite) "
                "VALUES (:panier_id, :produit_id, :quantite)",
                {'panier_id': panier_id, 'produit_id': produit['ProduitId'], 'quantite': quantite}
            )

        # Sauvegarder les modifications dans la base de données
        db.session.commit()

        # Retourner une réponse de succès
        return jsonify({"msg": "Produit ajouté au panier avec succès", "data": {"ProduitId": produit['ProduitId'], "Quantite": quantite}})

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    
@shoppingCard_bp.route('/<productOffer_id>', methods=['DELETE'])
@etudiant_required
def delete_product_from_shopping_card(current_user, productOffer_id):
    try:
        # Récupérer le panier de l'utilisateur actuel
        panier = db.session.execute(
            "SELECT PanierId FROM Panier WHERE FK_EtudiantId = :etudiant_id",
            {'etudiant_id': current_user['id']}
        ).fetchone()

        if not panier:
            return jsonify({"error": "Panier non trouvé pour cet utilisateur"}), 404

        # Vérifier si le produit est dans le panier de l'utilisateur
        panier_item = db.session.execute(
            "SELECT * FROM PanierItem WHERE PK_PanierId = :panier_id AND PK_ProduitId = :product_id",
            {'panier_id': panier.PanierId, 'product_id': productOffer_id}
        ).fetchone()

        if not panier_item:
            return jsonify({"error": "Produit non trouvé dans le panier"}), 404

        # Supprimer l'élément du panier
        db.session.execute(
            "DELETE FROM PanierItem WHERE PK_PanierId = :panier_id AND PK_ProduitId = :product_id",
            {'panier_id': panier.PanierId, 'product_id': productOffer_id}
        )

        # Sauvegarder les modifications dans la base de données
        db.session.commit()

        return jsonify({"msg": "Produit supprimé du panier avec succès", "data": {"ProduitId": productOffer_id}})
    
    except SQLAlchemyError as e:
        db.session.rollback()  # Effectuer un rollback en cas d'erreur
        error = str(e.__dict__['orig'])  # Récupérer le message d'erreur spécifique
        return jsonify({"error": error}), 500

@shoppingCard_bp.route('', methods=['GET'])
@etudiant_required
def get_shopping_card(current_user):
    try:
        # Récupérer le panier de l'utilisateur actuel
        panier = db.session.execute(
            "SELECT PanierId FROM Panier WHERE FK_EtudiantId = :etudiant_id",
            {'etudiant_id': current_user['id']}
        ).fetchone()

        if not panier:
            return jsonify({"error": "Panier non trouvé pour cet utilisateur"}), 404

        # Récupérer tous les produits dans le panier de l'utilisateur
        panier_items = db.session.execute(
            "SELECT p.ProduitId, p.Nom, p.Prix, pi.Quantite "
            "FROM PanierItem pi "
            "JOIN Produit p ON pi.PK_ProduitId = p.ProduitId "
            "WHERE pi.PK_PanierId = :panier_id",
            {'panier_id': panier.PanierId}
        ).fetchall()

        if not panier_items:
            return jsonify({"msg": "Le panier est vide"}), 200

        # Formater la réponse pour retourner les produits dans le panier
        items = []
        for item in panier_items:
            items.append({
                "ProduitId": item.ProduitId,
                "Nom": item.Nom,
                "Prix": item.Prix,
                "Quantite": item.Quantite
            })

        return jsonify({"msg": "Produits récupérés avec succès", "data": items}), 200
    
    except SQLAlchemyError as e:
        db.session.rollback()  # Annuler la transaction en cas d'erreur
        error = str(e.__dict__['orig'])  # Récupérer le message d'erreur spécifique
        return jsonify({"error": error}), 500

@shoppingCard_bp.route('/purchase', methods=['POST'])
@etudiant_required
def purchase_order(current_user):
    try:
        # Vérifier si l'utilisateur a un panier
        panier = db.session.execute(
            "SELECT PanierId FROM Panier WHERE FK_EtudiantId = :etudiant_id",
            {'etudiant_id': current_user['id']}
        ).fetchone()

        if not panier:
            return jsonify({"error": "Aucun panier trouvé pour cet utilisateur"}), 404

        # Récupérer les produits dans le panier de l'utilisateur
        panier_items = db.session.execute(
            "SELECT pi.PK_ProduitId, pi.Quantite, p.Stock, p.Prix "
            "FROM PanierItem pi "
            "JOIN Produit p ON pi.PK_ProduitId = p.ProduitId "
            "WHERE pi.PK_PanierId = :panier_id",
            {'panier_id': panier.PanierId}
        ).fetchall()

        # Créer la commande d'achat
        db.session.execute(
            "INSERT INTO Commande (FK_EtudiantId, DateCommande, Statut) "
            "VALUES (:etudiant_id, NOW(), 'En cours')",
            {'etudiant_id': current_user['id']}
        )
        db.session.commit()

        # Récupérer l'ID de la commande créée
        commande_id = db.session.execute(
            "SELECT LAST_INSERT_ID()"
        ).fetchone()[0]

        # Ajouter les produits de la commande à la table des commandes
        for item in panier_items:
            db.session.execute(
                "INSERT INTO CommandeItem (FK_CommandeId, FK_ProduitId, Quantite) "
                "VALUES (:commande_id, :produit_id, :quantite)",
                {'commande_id': commande_id, 'produit_id': item.PK_ProduitId, 'quantite': item.Quantite}
            )

            # Mettre à jour les stocks des produits
            db.session.execute(
                "UPDATE Produit SET Stock = Stock - :quantite WHERE ProduitId = :produit_id",
                {'quantite': item.Quantite, 'produit_id': item.PK_ProduitId}
            )

        # Sauvegarder les changements
        db.session.commit()

        # Suppression des articles du panier une fois la commande effectuée
        db.session.execute(
            "DELETE FROM PanierItem WHERE PK_PanierId = :panier_id",
            {'panier_id': panier.PanierId}
        )
        db.session.commit()

        return jsonify({"msg": "Commande passée avec succès", "commande_id": commande_id}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        error = str(e.__dict__['orig'])
        return jsonify({"error": error}), 500
    pass
