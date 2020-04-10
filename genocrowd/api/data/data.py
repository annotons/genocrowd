# from flask import current_app as ca
from flask import Blueprint, request

data_bp = Blueprint('data', __name__, url_prefix='/')


@data_bp.route('/api/data/selectedgenes', methods=["POST"])
def gff_from_apollo():
    file = request.files['file']
    print(file)
