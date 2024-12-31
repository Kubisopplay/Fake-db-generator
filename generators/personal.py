import faker


import datetime
#constraints that require a variable input like name should be the same as a generator name that generates expected input




generators = generators_dict.keys()

def get_name(**kwargs):
    if "locale" in kwargs:
        locale = kwargs["locale"]
    else:
        locale = "pl_PL"
    
    gender = kwargs["gender"]
    fake = faker.Faker(locale)
    if gender == "male":
        return fake.name_male().split()[0]
    elif gender == "female":
        return fake.name_female().split()[0]
    else:
        return fake.name_nonbinary().split()[0]
    

def get_surname(  **kwargs):
    if "locale" in kwargs:
        locale = kwargs["locale"]
    else:
        locale = "pl_PL"
    
    gender = kwargs["gender"]
    fake = faker.Faker(locale)
    if gender == "male":
        return fake.name_male().split()[1]
    elif gender == "female":
        return fake.name_female().split()[1]
    else:
        return fake.name_nonbinary().split()[1]


def get_pesel( **kwargs):
    fake = faker.Faker(locale="pl_PL")
    birth_date = datetime.datetime.strptime(kwargs["birth_date"], "%Y-%m-%d")
    pesel = fake.pesel(date_of_birth=birth_date,sex=kwargs["gender"]) #please dont cancel me, its just a mental shortcut
    return pesel


def get_nip( **kwargs):
    fake = faker.Faker(locale="pl_PL")
    return fake.nip()   


def get_email( **kwargs):
    fake = faker.Faker()
    return fake.email()
    
generators_dict = { 
    "name": {"description": "Generates a random name", "constraints" : ["gender", "locale"],"function": get_name},
    "surname": {"description": "Generates a random surname", "constraints" : ["gender", "locale"],"function": get_surname},
    "pesel": {"description": "Generates a random PESEL number. Requires gender and birth year", "constraints":["gender", "birth_date"],"function": get_pesel},
    "nip": {"description": "Generates a random tax registration number from Poland", "constraints": [], "function": get_nip},
    "email": {"description": "Generates a random email address. Constraints are used to link it to name and surname columns.",
              "constraints": ["name", "surname"], "function": get_email},
}