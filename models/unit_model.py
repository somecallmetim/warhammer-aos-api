from db import db


class UnitModel(db.Model):
    # tells sqlalchemy the name of the table
    __tablename__ = "units"

    # sets up data fields for sqlalchemy
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(255), unique=True)
    minimum_models = db.Column(db.SmallInteger)
    maximum_models = db.Column(db.SmallInteger)
    points_per_model = db.Column(db.SmallInteger)
    save = db.Column(db.SmallInteger)
    bravery = db.Column(db.SmallInteger)
    wounds = db.Column(db.SmallInteger)
    spells_per_round = db.Column(db.SmallInteger)

    # TODO faction_id

    def __init__(self, name, minimum_models, maximum_models, points_per_model, save, bravery, wounds, spells_per_round):
        self.unit_name = name
        self.minimum_models = minimum_models
        self.maximum_models = maximum_models
        self.points_per_model = points_per_model
        self.save = save
        self.bravery = bravery
        self.wounds = wounds
        self.spells_per_round = spells_per_round

    # returns a string representation of the unit in json format
    def json(self):
        return {
            "unit_name": self.unit_name, "minimum_models": self.minimum_models, "maximum_models": self.maximum_models,
            "points_per_model": self.points_per_model, "save": self.save, "bravery": self.bravery, "wounds": self.wounds,
            "spells_per_round": self.spells_per_round
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(unit_name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()