from melta.dynamic.propertyMaker import PropertyMaker

property_maker = PropertyMaker()


class Person:
    pass


person1 = Person()

property_maker.buildProperty(person1, "edad", 20) \
    .buildProperty(person1, "altura", 180) \
    .buildProperty(person1, "sexo", "male")


class House:
    pass


house1 = House()
property_maker.buildProperty(house1, "antiguedad", 32) \
    .buildProperty(house1, "tipo_casa", "bungalow") \
    .buildProperty(house1, "mt2", 360)

house2 = House()
property_maker.buildProperty(house2, "building_age", 34) \
    .buildProperty(house2, "material", "brick") \
    .buildProperty(house2, "sq2mts", 453)