import faker


import datetime
#constraints that require a variable input like name should be the same as a generator name that generates expected input
generators_dict = { 
    "name": {"description": "Generates a random name", "constraints" : ["gender", "locale"]},
    "surname": {"description": "Generates a random surname", "constraints" : ["gender", "locale"]},
    "pesel": {"description": "Generates a random PESEL number. Requires gender and birth year", "constraints":["gender", "birth_date"]},
    "nip": {"description": "Generates a random tax registration number from Poland", "constraints": []},
    "email": {"description": "Generates a random email address. Constraints are used to link it to name and surname columns.", "constraints": ["name", "surname"]},
}



generators = generators_dict.keys()

def get_name(gender, locale = "pl_PL", **kwargs):
    fake = faker.Faker(locale)
    if gender == "male":
        return fake.name_male().split()[0]
    elif gender == "female":
        return fake.name_female().split()[0]
    else:
        return fake.name_nonbinary().split()[0]
    

def get_surname( gender, locale = "pl_PL", **kwargs):
    fake = faker.Faker(locale)
    if gender == "male":
        return fake.name_male().split()[1]
    elif gender == "female":
        return fake.name_female().split()[1]
    else:
        return fake.name_nonbinary().split()[1]


def get_pesel(gender, birth_date, **kwargs):
    fake = faker.Faker(locale="pl_PL")
    birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
    pesel = fake.pesel(date_of_birth=birth_date,sex=gender) #please dont cancel me, its just a mental shortcut
    return pesel
def get_nip( **kwargs):
    fake = faker.Faker(locale="pl_PL")
    return fake.nip()


def get_email(name_column, surname_column, **kwargs):
    fake = faker.Faker()
    

    