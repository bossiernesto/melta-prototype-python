from melta.dynamic.propertyMaker import PropertyMaker

property_maker = PropertyMaker()


class Person:
    pass


persona1 = Person()

property_maker.buildProperty(persona1, "edad", 20)
property_maker.buildProperty(persona1, "altura", 180)
property_maker.buildProperty(persona1, "sexo", "masculino")


class Casa:
    pass


casa1 = Casa()
property_maker.buildProperty(casa1, "antiguedad", 32)
property_maker.buildProperty(casa1, "tipo_casa", "dos_aguas")
property_maker.buildProperty(casa1, "mt2", 360)


