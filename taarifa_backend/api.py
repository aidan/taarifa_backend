import json
from pprint import pformat

from flask import request, jsonify, render_template, make_response
from flask.ext.security import (Security, MongoEngineUserDatastore,
                                http_auth_required)
import mongoengine

import models
from models import BasicReport, Reportable
from taarifa_backend import app, db
from utils import crossdomain, jsonp
import _help

logger = app.logger

user_datastore = MongoEngineUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)


def get_services():
    response = {}

    services = models.get_available_services()
    for service_description in services:
        logger.debug(service_description)
        service_name = str(service_description.__name__)
        logger.debug(service_name)

        fields = service_description._fields
        logger.debug(fields)

        service = {}
        field_dict = {}
        for name, f in fields.iteritems():
            if name in ['id', 'created_at']:
                continue
            field = {}
            field['required'] = str(f.required)
            field['type'] = _help.db_type_to_string(f.__class__)
            field_dict[name] = field
        service['fields'] = field_dict
        for key in ['protocol_type', 'keywords', 'service_name',
                    'service_code', 'group', 'description']:
            service[key] = getattr(service_description, key)
        logger.debug(service)
        response[service_name] = service
    return response


@app.route("/")
def landing():
    return render_template('landing.html', services=pformat(get_services()))


@app.route("/reports", methods=['POST'])
@crossdomain(origin='*', headers="Origin, X-Requested-With, Content-Type, Accept")
def receive_report():
    """
    post report to the backend
    """
    logger.debug('Report post received')
    logger.debug('JSON: ' + request.json.__repr__())

    # TODO: Deal with errors regarding a non existing service code
    service_code = request.json['service_code']
    service_class = models.get_service_class(service_code)

    # TODO: Handle errors if the report field is not available
    data = request.json['data']
    data.update(dict(service_code=service_code))
    logger.debug(data.__repr__())
    db_obj = service_class(**data)
    logger.debug(db_obj.__unicode__())

    try:
        doc = db_obj.save()
    except mongoengine.ValidationError, e:
        logger.debug(e)
        # TODO: Send specification of the service used and a better error
        # description
        return jsonify({'Error': 'Validation Error'})

    return jsonify(_help.mongo_to_dict(doc))


@app.route("/reports", methods=['GET'])
@crossdomain(origin='*')
@jsonp
def get_all_reports():
    logger.debug(request.args.__repr__())
    service_code = request.args.get('service_code', None)

    service_class = models.get_service_class(
        service_code) if service_code else Reportable

    all_reports = service_class.objects.all() if service_class else []

    result = map(_help.mongo_to_dict, all_reports)
    return make_response(json.dumps(result))


@app.route("/reports/<string:id>", methods=['GET'])
@crossdomain(origin='*')
@jsonp
def get_report(id=False):
    # TODO: This is still using BasicReport, should be moved to service based
    # world
    report = BasicReport.objects.with_id(id)
    return jsonify(_help.mongo_to_dict(report))


@app.route("/services", methods=['GET'])
@crossdomain(origin='*')
@jsonp
def get_list_of_all_services():
    # TODO: factor out the transformation from a service to json
    return jsonify(**get_services())


@app.route("/admin", methods=["POST"])
@http_auth_required
@crossdomain(origin='*', headers="Origin, X-Requested-With, Content-Type, Accept")
@jsonp
def create_admin():
    """
    create an admin in the backend
    """
    logger.debug('New admin received')
    logger.debug('JSON: ' + request.json.__repr__())

    # TODO: Deal with errors regarding a non existing service code
    required = ["email", "password"]
    missing = list(set(required) - set(request.json.keys()))
    if missing:
        response = jsonify({"Error": "Validation Error",
                            "Missing": missing})
        response.status_code = 422
        return response

    try:
        user = user_datastore.create_user(email=request.json["email"],
                                          password=request.json["password"])
    except mongoengine.ValidationError:
        return jsonify({'Error': 'Validation Error'})

    return jsonify(_help.mongo_to_dict(user))
