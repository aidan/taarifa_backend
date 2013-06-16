import datetime
from flask import url_for
from taarifa_backend import db


class Metadata(object):
    """
    Description of a service
    """
    def __init__(self, service_code, service_name, description, group=None):
        self.service_code = service_code
        self.service_name = service_name
        self.description = description
        self.group = group

    def __repr__(self):
        return 'Metadata(' + ','.join(map(str, [self.service_code, self.service_name, self.description, self.group])) + ')'


class Reportable(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    latitude = db.FloatField(required=True)
    longitude = db.FloatField(required=True)

    meta = {'allow_inheritance': True}


class Waterpoint(Reportable):
    # Duplication of ids because the waterpoint dataset already contains ids
    waterpoint_id = db.StringField(required=True)
    functional = db.BooleanField(required=True)

    #potentially add a type field to describe the type of waterpoint reported on

    metadata = Metadata('wp001', 'Waterpoint', 'Location, description and functionality of a waterpoint', 'water')

    # TODO: Unsure how to best handle the service code logic
    service_code = db.StringField(default=metadata.service_code, required=True)
    def __unicode__(self):
        return 'Waterpoint(' + ','.join(map(str, [self.latitude, self.longitude, self.functional, self.waterpoint_id])) + ')'


class BasicReport(Reportable):
    title = db.StringField(max_length=255, required=True)
    desc = db.StringField(required=False)

    # TODO: Move the descriptive fields into a metadata dictionary/object
    description = "Basic location based report"
    keywords = ['basic', 'location', 'report']
    group = 'location based reports'
    service_name = 'basic report'
    service_code = '0001'
    protocol_type = None

    meta = {'allow_inheritance': True}

    def __unicode__(self):
        return ','.join(map(str, [self.created_at, self.title, self.desc, self.latitude, self.longitude]))


class AdvancedReport(BasicReport):
    complicated_information = db.StringField(max_length=255, required=False)
    advanced_stuff = db.StringField(required=False)
    advanced_date = db.DateTimeField(required=False)

    description = "Extension of the Basic Report"
    keywords = ['advanced', 'cool', 'report', 'location']
    service_name = 'advanced report'
    service_code = '0002'

service_codes = {'wp001': Waterpoint,
                 '0001': BasicReport,
                 '0002': AdvancedReport,
                }

def get_available_services():
    return [BasicReport, AdvancedReport]

def get_service_class(service_code):
    return service_codes.get(service_code, None)
