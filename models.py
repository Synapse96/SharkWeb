from mongoengine import Document, IntField, StringField, DictField


class HighSchool(Document):
    id = IntField(required=True, primary_key=True)
    name = StringField(required=True)
    street = StringField(required=True)
    suburb = StringField(required=True)
    postcode = IntField(required=True)
    attendance_rates = DictField(required=True)

    def __init__(self, id, name, street, suburb, postcode, attendance_rates, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.name = name
        self.street = street
        self.suburb = suburb
        self.postcode = postcode
        self.attendance_rates = attendance_rates
