from flask_restful import Resource, reqparse
from models.unit_model import UnitModel


class UnitList(Resource):
    def get(self):
        return {"units": [unit.json() for unit in UnitModel.query.all()]}


class UnitResource(Resource):
    # parser will collect and parse any json sent by the client
    parser = reqparse.RequestParser()
    # sets up parser to accept only data we want from the json sent by the client
    parser.add_argument("minimum_models", type=int, required=True, help="This field is required")
    parser.add_argument("maximum_models", type=int, required=True, help="This field is required")
    parser.add_argument("points_per_model", type=int, required=True, help="This field is required")
    parser.add_argument("save", type=int, required=True, help="This field is required")
    parser.add_argument("bravery", type=int, required=True, help="This field is required")
    parser.add_argument("wounds", type=int, required=True, help="This field is required")
    parser.add_argument("spells_per_round", type=int, required=True, help="This field is required")

    def get(self, name):
        # check to see if unit is in the db
        unit = UnitModel.find_by_name(name)
        # return unit if found
        if unit:
            return unit.json()
        # send error message if not
        return {"message": "Unit not found... :( "}, 404

    def post(self, name):
        # check to see if unit is in the db
        unit = UnitModel.find_by_name(name)
        # return error if unit is in db
        if unit:
            return {"message": "A unit by the name '{}' already exists. :(".format(name)}, 400

        # get and parse json data sent by client
        data = UnitResource.parser.parse_args()
        # create new UnitModel object
        unit = UnitModel(name, **data)

        # attempt to persist new UnitModel object to database
        try:
            unit.save_to_db()
        except:
            return {"message": "an error occured while inserting the item"}, 500

        # return persisted unit and http status code
        return unit.json(), 201

    def put(self, name):
        # check if unit exists in db
        unit = UnitModel.find_by_name(name)

        # get and parse json data sent by client
        data = UnitResource.parser.parse_args()

        # if the unit was already in the db, update the unit
        if unit:
            # populate units data fields with new data
            for data_field in unit.unit_data:
                unit.unit_data[data_field] = data[data_field]
            # attempt to persist updated UnitModel to database
            try:
                unit.save_to_db()
            except:
                return {"message": "an error occured while inserting the item"}, 500

        # if unit was not in db, create new unit
        else:
            # create new UnitModel object
            unit = UnitModel(name, **data)
            # attempt to persist new UnitModel object to database
            try:
                unit.save_to_db()
            except:
                return {"message": "an error occured while inserting the item"}, 500
            return unit, 201

    def delete(self, name):
        # check to see if unit exists in database
        unit = UnitModel.find_by_name(name)
        # if unit exists, remove from database
        if unit:
            unit.delete_from_db()
            return {"message": "unit successfully deleted"}
        # return error message and http status code if unit doesn't exists
        return {"message": "item not found"}, 404