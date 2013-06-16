from taarifa_backend.api import get_all_reports
from taarifa_backend import db


ftypes = {
    'string': db.StringField,
    'boolean': db.BooleanField,
    'integer': db.IntField,
    'float': db.FloatField,
    'datetime': db.DateTimeField,
    }

class ReportField(db.Document):
    """
    Describes the specifications of field in a report
    """
    name = db.StringField(required=True)
    ftype = db.StringField(required=True, choices=ftypes.keys())
    required = db.BooleanField(default=False)


class Service(db.Document):
    """
    Description of the format of the data for a given report

    @param name: Human readable name of the service
    @param description: description of the service
    @param fields: The list of fields which are available for a
        report of this service
    """
    name = db.StringField(required=True)
    description = db.StringField(required=True)
    fields = db.ListField(field=db.ReferenceField(ReportField))


def create_db_field(report_field):
    db_field = ftypes[report_field.ftype]
    required = report_field.required
    return db_field(required=required)


def create_model(service):
    """
    takes a service object and creates the corresponding reportable
    which can then be used to save a report for the given service
    """
    # TODO: How to name the report model automatically such that there are
    # no clashes? For the moment use the user defined service_name
    # Have to check if service.name is a legal python class name
    # TODO: Inherit from reportable
    # TODO: Field names must be allowed attribute names in python!
    fields = dict([(f.name, create_db_field(f)) for f in service.fields])
    return type(service.name, (db.Document, ), fields)


def example():
    # Create a service for waterpoints dynamically
    service_name = 'Waterpoint'
    desc = 'Collection of waterpoints'
    field1 = ReportField(name='waterpoint_id', ftype='string')
    field2 = ReportField(name='functional', ftype='boolean', required=True)
    field3 = ReportField(name='number_of_people_served', ftype='integer')
    fields = [field1, field2, field3]
    for f in fields:
        f.save()
    s = Service(name=service_name, description=desc, fields=fields)
    s.save()

    objs = Service.objects.all()
    print 'Stored services are:'
    for o in objs:
        print o.to_mongo()

    # Convert the service into a db.Document class
    db_class = create_model(s)
    # save a new report for this service
    data = dict(number_of_people_served=28, functional=True,
            waterpoint_id='wp_001')
    obj = db_class(**data)
    obj.save()

    reports = db_class.objects.all()
    print 'Saved report for this service are:'
    for r in reports:
        print r.to_mongo()

if __name__ == '__main__':
    example()
