from melta.dynamic.propertyMaker import PropertyMaker

property_maker = PropertyMaker()


class Person:
    pass


person1 = Person()

property_maker.buildProperty(person1, "edad", 20)
property_maker.buildProperty(person1, "altura", 180)
property_maker.buildProperty(person1, "sexo", "male")


class House:
    pass


house1 = House()
property_maker.buildProperty(house1, "antiguedad", 32)
property_maker.buildProperty(house1, "tipo_casa", "bungalow")
property_maker.buildProperty(house1, "mt2", 360)


