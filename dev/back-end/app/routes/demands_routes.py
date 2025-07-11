from flask import Blueprint
from app.routes.decorators.authDecorators import annonceur_required

demands_bp = Blueprint('demands', __name__)

@demands_bp.route('/jobOffers', methods=['GET'])
@annonceur_required
def get_job_offers_demands():
    # Placeholder for fetching job offers demands logic
    pass

@demands_bp.route('/housingOffers', methods=['GET'])
@annonceur_required
def get_housing_offers_demands():
    # Placeholder for fetching housing offers demands logic
    pass

@demands_bp.route('', methods=['GET'])
@annonceur_required
def get_demands():
    # Placeholder for fetching all demands logic
    pass
