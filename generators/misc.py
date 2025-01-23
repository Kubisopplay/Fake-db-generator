
from guidancestuff import loaded_model
from guidance import system, user, assistant, gen, select
import random

last_id = -1

def id_generator(**kwargs):
    global last_id
    last_id += 1
    return last_id 

def reset_id():
    global last_id
    last_id = -1
    
def universal_generator(**kwargs):
    if "suggestion" in kwargs:
        suggestion = kwargs["suggestions"]
    else:
        suggestion = "No suggestion"
    lm = loaded_model
    with system():
        lm += "You are a random data generator. You have to generate a plausible value for a field in a database. The field is described by its name, type, and additional properties.\
            The generator is a universal generator, it can generate any type of data, but its very slow.\
                The user will give you a suggestion of what the data should look like.\
                    You should generate a value that fits the suggestion.\
                Remember to only answer with the value so the code does not break. "
    with user():
        lm += "I need a value for a field in a database. The field is described by its name, type, and additional properties.\
            I need a value that fits the suggestion I will give you.\
                The suggestion is: " + suggestion
    with assistant():
        lm += "The value generated is: " + gen(name="universal_generator") + "."
    return lm["universal_generator"]


generators_dict ={
    "id_generator": {"description": "Generates a unique id, starting from 0", "constraints": [], "function": id_generator},
    "universal_generator" : {
        "description" : "Generates a value based on a suggestion, its very slow, avoid using it if possible",
        "constraints" : ["suggestion"],
        "function" : universal_generator
    }
}


generators = generators_dict.keys()
