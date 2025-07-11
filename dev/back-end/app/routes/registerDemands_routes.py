from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app.routes.decorators.authDecorators import register_validator_required
from app.db import db
import app.utils.utile as Utile
import app.services.mailSever as mailServer

registerDemands_bp = Blueprint('registerDemands', __name__)

@registerDemands_bp.route('/refuse', methods=['POST'])
@register_validator_required
def refuse_register_demand(admin):
    data = request.get_json() or {}
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Check if the user exists and has a 'toVerifyByAdmin' status
    check_query = text("""
        SELECT Email, Status,Nom 
        FROM Etudiant 
        WHERE Email = :email AND Status = 'toVerifyByAdmin'
        
        UNION
        
        SELECT Email, Status,Nom
        FROM Annonceur 
        WHERE Email = :email AND Status = 'toVerifyByAdmin'
    """)
    user = db.session.execute(check_query, {"email": email}).mappings().first()

    if not user:
        return jsonify({'error': 'User not found or already verified'}), 404

    # Update the user's status to 'disabled'
    delete_query_etudiant = text("delete from etudiant WHERE Email = :email")
    delete_query_annonceur = text("delete from annonceur  WHERE Email = :email")

    rows_affected = 0
    if user["Email"] in [r[0] for r in db.session.execute(text("SELECT Email FROM Etudiant")).fetchall()]:
        rows_affected = db.session.execute(delete_query_etudiant, {"email": email}).rowcount
    elif user["Email"] in [r[0] for r in db.session.execute(text("SELECT Email FROM Annonceur")).fetchall()]:
        rows_affected = db.session.execute(delete_query_annonceur, {"email": email}).rowcount

    if rows_affected == 0:
        return jsonify({'error': 'Failed to refuse registration demand'}), 500

    db.session.commit()
    activation_mail=mailServer.create_activation_notification_body(user['Email'],user['Nom'],False)
    mailServer.send_email(user['Email'],activation_mail,"Account Activation")

    

    return jsonify({'message': 'Registration demand refused successfully'}), 200


@registerDemands_bp.route('/accept', methods=['POST'])
@register_validator_required
def accept_register_demand(admin):
    data = request.get_json() or {}
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Check if the user exists and has a 'toVerifyByAdmin' status
    check_query = text("""
        SELECT Email, Status,Nom 
        FROM Etudiant 
        WHERE Email = :email AND Status = 'toVerifyByAdmin'
        
        UNION
        
        SELECT Email, Status,Nom 
        FROM Annonceur 
        WHERE Email = :email AND Status = 'toVerifyByAdmin'
    """)
    user = db.session.execute(check_query, {"email": email}).mappings().first()

    if not user:
        return jsonify({'error': 'User not found or already verified'}), 404

    # Update the user's status to 'active'
    update_query_etudiant = text("UPDATE Etudiant SET Status = 'active' WHERE Email = :email")
    update_query_annonceur = text("UPDATE Annonceur SET Status = 'active' WHERE Email = :email")

    rows_affected = 0
    if user["Email"] in [r[0] for r in db.session.execute(text("SELECT Email FROM Etudiant")).fetchall()]:
        rows_affected = db.session.execute(update_query_etudiant, {"email": email}).rowcount
    elif user["Email"] in [r[0] for r in db.session.execute(text("SELECT Email FROM Annonceur")).fetchall()]:
        rows_affected = db.session.execute(update_query_annonceur, {"email": email}).rowcount

    if rows_affected == 0:
        return jsonify({'error': 'Failed to accept registration demand'}), 500

    db.session.commit()
    activation_mail=mailServer.create_activation_notification_body(user['Email'],user['Nom'])
    mailServer.send_email(user['Email'],activation_mail,"Account Activation")

    return jsonify({'message': 'Registration demand accepted successfully'}), 200



@registerDemands_bp.route('', methods=['GET'])
@register_validator_required
def get_register_demands(admin):
    # Fetch Etudiant demands
    etudiant_query = text("""
        SELECT 
            EtudiantId AS id,
            justificationDocument,
            CarteNationale,
            ConterInteret,
            Email,
            EtablissementScolaire,
            Nom,
            Prenom,
            Profile_Image,
            Telephone,
            Ville,
            Status,
            'Etudiant' AS type
        FROM Etudiant 
        WHERE Status = 'toVerifyByAdmin'
    """)
    etudiant_results = db.session.execute(etudiant_query).mappings().all()

    # Convert RowMapping objects to dictionaries for Etudiant results
    server_ip, server_port = Utile.get_request_server_port(request)
    etudiant_list = []
    for result in etudiant_results:
        etudiant_dict = dict(result)
        
        # Generate server paths for specific fields
        etudiant_dict['justificationDocument'] =Utile.get_account_file_url(server_ip, server_port, etudiant_dict['justificationDocument'])
        etudiant_dict['CarteNationale'] = Utile.get_account_file_url(server_ip, server_port, etudiant_dict['CarteNationale'])
        etudiant_dict['Profile_Image'] = Utile.get_account_file_url(server_ip, server_port, etudiant_dict['Profile_Image'])
        
        etudiant_list.append(etudiant_dict)

    # Fetch Annonceur demands
    annonceur_query = text("""
        SELECT 
            AnnonceurId AS id,
            CarteNationale,
            Email,
            Nom,
            Prenom,
            Profile_Image,
            Telephone,
            Ville,
            Status,
            'Annonceur' AS type
        FROM Annonceur 
        WHERE Status = 'toVerifyByAdmin'
    """)
    annonceur_results = db.session.execute(annonceur_query).mappings().all()

    # Convert RowMapping objects to dictionaries for Annonceur results
    annonceur_list = []
    for result in annonceur_results:
        annonceur_dict = dict(result)
        
        # Generate server paths for specific fields
        annonceur_dict['CarteNationale'] = Utile.get_account_file_url(server_ip, server_port, annonceur_dict['CarteNationale'])
        annonceur_dict['Profile_Image'] = Utile.get_account_file_url(server_ip, server_port, annonceur_dict['Profile_Image'])
        
        annonceur_list.append(annonceur_dict)

    # Combine the results into a single list
    register_demands = etudiant_list + annonceur_list

    return jsonify({
        "etudiants": etudiant_list,
        "annonceurs": annonceur_list,
        "demands": register_demands
    }), 200