import guidance
from guidance.models import Transformers
from guidance import system, user, assistant, gen, select
from guidancestuff import loaded_model
from generators import personal, misc

tools = {}

tools.update(personal.generators_dict)
tools.update(misc.generators_dict)



def format_all_fields(all_fields):
    return "\n".join([f"{field['name']}: {field['type']} {field['rest']}" for field in all_fields])

def format_all_generators(all_generators):
    return "\n".join([f"{generator}: {all_generators[generator]['description']}" for generator in all_generators.keys()])

def constraints_intra_table(all_fields, all_generators,):
    lm = loaded_model
    with system():
        lm += f"You are a database administrator and you need to generate a value for a field in a database. The field is described by its name, type, and additional properties.\
            The generator has a set of constraints that define what value will it generate. \
            They should be used to generate a coherent set of values for a row in the table. \
            For example, if there is a field \
            The table has the following fields: {format_all_fields(all_fields)} \
            You have the following generators: {format_all_generators(all_generators)}"
            
    prompt_prepared = lm
    results = {}
    for field in all_fields:
        lm = prompt_prepared    
        with user():
            lm += f"I have a field named {field['name']} of type {field['type']} with additional properties {field['rest']}."
        with assistant():
            lm += f"Thinking about this step by step," + gen("Thoth")
            lm += f"Based on the field's name, type, and additional properties, I think the best generator for this field is" + select(all_generators.keys(), "tool") + "."
            lm += f"The generator has the following constraints: {all_generators[lm['tool']]['constraints']}"
            constraints = []
            for constraint in all_generators[lm['tool']]['constraints']:
                lm += f"Based on the data gathered, I think the best value for the constraint {constraint} is" + gen(f"constraint_value_{constraint}")
                constraints.append(lm[f"constraint_value_{constraint}"])
            results[field['name']] = (lm['tool'], constraints)
    return results
    
mock_table = [{"name": "id", "type": "INT", "rest": "PRIMARY KEY"},
                {"name": "name", "type": "VARCHAR(100)", "rest": "NOT NULL"},
                {"name": "surname", "type": "VARCHAR(510)", "rest": "NOT NULL"},
                {"name": "email", "type": "VARCHAR(100)", "rest": "NOT NULL"}]

if __name__ == "__main__":
    print(constraints_intra_table(mock_table, tools))
    