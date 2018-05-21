from mongoengine import Document, IntField, StringField, DictField


class HighSchool(Document):
    id = IntField(required=True, primary_key=True)
    name = StringField(required=True)
    street = StringField(required=True)
    suburb = StringField(required=True)
    postcode = IntField(required=True)
    students = IntField(required=True)
    selective = StringField(required=True)
    gender = StringField(required=True)
    attendance_rates = DictField()
    selective_entry_scores = DictField()
    enrollments = DictField()

    def __init__(self, id, name, street, suburb, postcode, students, selective, gender, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.name = name
        self.street = street
        self.suburb = suburb
        self.postcode = postcode
        self.students = students
        self.selective = selective
        self.gender = gender
