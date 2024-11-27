import faker



generators_dict = {
    "name": {"description": "Generates a random name", "constraints" : ["gender", "locale"]},
    "surname": {"description": "Generates a random surname", "constraints" : ["gender", "locale"]},
    "pesel": {"description": "Generates a random PESEL number", "constraints":["gender", "birth_date"]},
    "nip": {"description": "Generates a random tax registration number from Poland", "constraints": []},
    "email": {"description": "Generates a random email address", "constraints": ["name", "surname"]}
}

generators = generators_dict.keys()

def get_name(gender, locale = "pl_PL"):
    pass

def get_surname( gender, locale = "pl_PL"):
    pass


def get_pesel(gender, birth_date):
    pass

def get_nip():
    pass

def get_email(name, surname):
    pass

    