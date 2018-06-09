from app import dao
from app.models import Letter
from flask_restful import Resource, fields, marshal_with


class CityApi(Resource):
    city_fields = {
        "id":fields.Integer,
        "parentId":fields.Integer,
        "refionName":fields.String,
        "cityCode":fields.Integer,
        "pinYin":fields.String
    }
    value_fields = {
        # "A":fields.Nested(city_fields)
    }
    out_fields = {
        "returnCode":fields.String(default=0),
        "returnValue":fields.Nested(value_fields)
    }
    @marshal_with(out_fields)
    def get(self):
        letters = dao.queryAll(Letter)
        # print(letters)
        returnValue = {}
        for letter in letters:
            self.value_fields[letter.name] = fields.Nested(self.city_fields)
            returnValue[letter.name]=letter.citys
            print(letter.citys)

        return {'returnValue':returnValue}
