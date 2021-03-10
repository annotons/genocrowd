# from flask import current_app as ca
from BCBio import GFF

from flask import Blueprint, request, session
from flask import current_app as ca

from genocrowd.api.auth.login import admin_required
from genocrowd.libgenocrowd.Data import Data

import gridfs

import tempfile

from io import StringIO


data_bp = Blueprint('data', __name__, url_prefix='/')


@data_bp.route('/api/data/uploadgenes', methods=["POST"])
@admin_required
def gene_from_apollo():
    """ Receives the GFF file from the client:
        - Splits the genes in separate GFF files
        - Saves them in the database
    Returns
    -------

    json
        error
        errorMessage
    """
    db = ca.mongo.db
    fs = gridfs.GridFS(db, collection="genes")
    file = request.files['file']
    with tempfile.NamedTemporaryFile(mode='w+') as full_gff:
        file.save(full_gff.name)
        result = {
            'error': False,
            'errorMessage': "",
        }
        count = 1
        for rec in GFF.parse(full_gff):
            gene_list = rec.features
            for gene in gene_list:
                rec.annotations = {}
                rec.seq = ""
                rec.features = [gene]
                gff_out = StringIO()
                GFF.write([rec], gff_out)
                fs.put(gff_out.getvalue().encode(), _id=gene.id, chromosome=rec.id, start=gene.location.start, end=gene.location.end, strand=gene.location.strand, isAnnotable=True)
                count += 1
    return result


@data_bp.route('api/data/getgenes', methods=["GET"])
@admin_required
def admin_get_genes():
    """ Gets all the genes in the database to display them in the admin tab

    Returns
    -------

    json
        error : Boolean
        errorMessage : str
        genes : List
    """
    dataInstance = Data(ca, session)
    gene_list = dataInstance.get_all_positions()
    result = {'error': False,
              'errorMessage': "",
              'genes': gene_list
              }
    return result


@data_bp.route('api/data/setannotable', methods=["POST"])
@admin_required
def set_annotable():
    """ set the received gene as Annotable in the database

    Returns
    -------

    json
        error : Boolean
        errorMessage : str
    """
    data = request.get_json()
    dataInstance = Data(ca, session)
    gene = dataInstance.update_position_info(data["gene"], "isAnnotable", data["newAnnot"])
    if gene["isAnnotable"] == data["newAnnot"]:
        result = {
            'error': False,
            'errorMessage': ""
        }
    else:
        result = {
            'error': True,
            'errorMessage': "No Update!"
        }
    return result


@data_bp.route('api/data/removegene', methods=["POST"])
@admin_required
def remove_gene_from_db():
    """ Remove the received gene from the database

    Returns
    -------

    json
        error : Boolean
        errorMessage : str
    """
    data = request.get_json()
    db = ca.mongo.db
    fs = gridfs.GridFS(db, collection="genes")
    fs.delete(data["_id"])
    result = {'error': False,
              'errorMessage': ""
              }
    return result
