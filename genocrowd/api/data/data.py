import tempfile
from io import StringIO

from BCBio import GFF

from flask import Blueprint, request, session
from flask import current_app as ca

from genocrowd.api.auth.login import admin_required, login_required
from genocrowd.libgenocrowd.Data import Data
from genocrowd.libgenocrowd.LocalAuth import LocalAuth

import gridfs


data_bp = Blueprint('data', __name__, url_prefix='/')


@data_bp.route('/api/data/uploadgenes', methods=["POST"])
@admin_required
def gene_from_apollo():
    """ Receives the GFF file from the client:
        - Splits the genes in separate GFF files
        - Add a priority to each genes
        - Calculates the difficulty of each genes
        - Saves them in the database
    Returns
    -------

    json
        error
        errorMessage
    """
    db = ca.mongo.db
    fs = gridfs.GridFS(db, collection="genes")
    priority = request.form['priority']
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
            nb_features = len(gene.sub_features)
            for gene in gene_list:
                # TODO change difficulty calculation
                difficulty = (gene.location.end - gene.location.start) - nb_features * 10
                rec.annotations = {}
                rec.seq = ""
                rec.features = [gene]
                gff_out = StringIO()
                GFF.write([rec], gff_out)
                fs.put(gff_out.getvalue().encode(), _id=gene.id, chromosome=rec.id, start=gene.location.start, end=gene.location.end, strand=gene.location.strand, isAnnotable=True, difficulty=difficulty, priority=priority, tags=[])
                count += 1

    # FIXME refresh gene list in UI
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


@data_bp.route('api/data/removeallgenes', methods=["GET"])
@admin_required
def remove_all_genes_from_db():
    """Remove all genes from de db

    Return
    ------
    json
        error : Boolean
        errorMessage: str
    """
    dataInstance = Data(ca, session)
    gene_list = dataInstance.get_all_positions()

    db = ca.mongo.db
    fs = gridfs.GridFS(db, collection="genes")

    for element in gene_list:
        fs.delete(element['_id'])

    result = {
        'error': False,
        'errorMessage': "",
    }
    return result


@data_bp.route('api/data/getanswersamount', methods=["GET"])
def get_answers_amount():
    """get the number of annotations in the database

    Return
    ------
    int
        Number of annotations
    """
    dataInstance = Data(ca, session)
    answers_amount = dataInstance.get_number_of_answers()
    result = {
        'error': False,
        'errorMessage': "",
        'answersAmount': answers_amount
    }
    return result


@data_bp.route('api/data/getusersamount', methods=["GET"])
def get_user_amount():
    """get the number of user in the database

    Returns
    -------
    int
        Number of user in the Database
    """
    dataInstance = LocalAuth(ca, session)
    users_amount = dataInstance.get_number_of_users()
    result = {
        'error': False,
        'errorMessage': "",
        'usersAmount': users_amount
    }
    return result


@data_bp.route('api/data/getgroupsamount', methods=['GET'])
def get_groups_amount():
    """get the number of groups in the database

    Returns
    -------
    int
        Number of groups in the database
    """
    dataInstance = Data(ca, session)
    groupsAmount = dataInstance.get_number_of_groups()
    result = {
        'error': False,
        'errorMessage': "",
        'groupsAmount': groupsAmount
    }
    return result


@data_bp.route('api/data/setgroupsamount', methods=['POST'])
@admin_required
def set_groups_amount():
    """Update the number of groups

    Returns
    -------
    dict
        error, error message and updated number of groups
    """
    data = request.get_json()
    dataInstance = Data(ca, session)
    result = dataInstance.set_number_of_groups(data)
    return result


@data_bp.route('api/data/updategroupname', methods=['POST'])
@admin_required
def update_group_name():
    """Update the name of a group

    Returns
    -------
    dict
        error, error message and group name
    """
    data = request.get_json()
    dataInstance = Data(ca, session)
    result = dataInstance.update_group_name(data)
    return result


@data_bp.route('/api/data/gettopannotation', methods=['GET'])
@login_required
def get_top_annotation():
    dataInstance = Data(ca, session)
    result = dataInstance.get_top_annotation()
    return result


@data_bp.route('/api/data/getgroupsnames', methods=['GET'])
@login_required
def get_groups_names():
    """ Get groups names

    Returns
    -------
        dict
            error, error message and list of groups names
    """
    dataInstance = Data(ca, session)
    result = dataInstance.get_groups_names()
    return result


@data_bp.route('/api/data/countallgenes', methods=['GET'])
@login_required
def count_all_genes():
    """Get the quantity of genes to annotate

    Returns
    -------
        dict
            error, error message and quantity of genes to annotate
    """
    error = False
    errorMessage = []
    dataInstance = Data(ca, session)
    result = dataInstance.count_all_genes()
    return {
        'error': error,
        'errorMessage': errorMessage,
        'genes': result
    }
