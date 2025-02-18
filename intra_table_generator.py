

from generators.personal import generators_dict as personal_generators_dict
from generators.misc import generators_dict as misc_generators_dict
from guidance import system, user, assistant, gen, select
from guidancestuff import load_model
from generators import personal, misc
from discriminator import get_best_tool
from multiprocessing import freeze_support

# get all constraints
# get all generators
# if any constraint is named the same as generator move them to a second list
# if any generator has a constraint that is not in the list of generators, move it to a third list
# generate values for nongenerator constraints
# generate values for generator constraints
#return the row 


all_generators = {}
all_generators.update(personal_generators_dict)
all_generators.update(misc_generators_dict)


def intra_table_generator(table):
    all_constraints_required = []
    all_generators_required = []
    generators_ordered = {}
    
    
    for field in table:
        best_tool = get_best_tool(field)
        all_generators_required.append(best_tool) 
        generators_ordered[field['name']] = best_tool
    
    for generator in all_generators_required:
        for constraint in all_generators[generator]['constraints']:
            all_constraints_required.append(constraint)
    
    intermediate_constraints = []
    primary_constraints = []
              
    for constraint in all_constraints_required:
        if constraint in all_generators:
            intermediate_constraints.append(constraint)
        else:
            primary_constraints.append(constraint)
        
    primary_constraints = list(set(primary_constraints))
    intermediate_constraints = list(set(intermediate_constraints))
    
    
    return primary_constraints, intermediate_constraints, all_generators_required, generators_ordered
        
        
def generate_row(primary_constraints, intermediate_constraints, all_generators_required, generators_ordered):
    lm = load_model()
    with system():
        primary_generator = lm + "You are a database administrator and you need to generate a value for a field in a database. The field is described by its name, type, and additional properties.\
            The generator has a set of constraints that define what value will it generate. \
            They should be used to generate a coherent set of values for a row in the table. \
            For example, if there is a field named locale of type VARCHAR(100) and additional properties NOT NULL, the generator should generate a locale name. \
            Remember to only answer the question so the code does not break. "


    constraints = {}
    for constraint in primary_constraints:
        with user():
            generator = primary_generator + "\r\nName of the constraint: " + constraint
            generator += " Remember to only answer the question, so the program processing it does not get confused"
        with assistant():
            generator += "Lets think this step by step " + gen("Thoth")
            generator += "My final answer for the value of the generator is: " + gen("value", temperature=0.4, max_tokens=20) + "."
        constraints[constraint] = generator["value"].strip().replace("\n", "").replace("\r", "").replace("\'", "").replace("\"", "").replace("  ", " ").replace("[", "").replace("]", "")
    
    for generator in intermediate_constraints:
        generator_constraints = all_generators[generator]
        temp = {}
        for constraint in generator_constraints["constraints"]:
            temp[constraint] = constraints[constraint]
        constraints[generator] = all_generators[generator]["function"](**temp)
        
    row = {}
    
    for field in generators_ordered:
        if generators_ordered[field] in constraints:
            row[field] = constraints[generators_ordered[field]]
        else:
            row[field] = all_generators[generators_ordered[field]]["function"](**constraints)
            
    return row


mock_table = [{"name": "id", "type": "INT", "rest": "PRIMARY KEY"},
                {"name": "name", "type": "VARCHAR(100)", "rest": "NOT NULL"},
                {"name": "surname", "type": "VARCHAR(510)", "rest": "NOT NULL"},
                {"name": "email", "type": "VARCHAR(100)", "rest": "NOT NULL"}]

mock_table2 = [{"name": "id", "type": "INT", "rest": "PRIMARY KEY"},
                {"name": "title", "type": "VARCHAR(255)", "rest": "NOT NULL"},
                {"name": "author", "type": "VARCHAR(255)", "rest": "NOT NULL"},
                {"name": "published_year", "type": "INT", "rest": "NOT NULL"},
                {"name": "genre", "type": "VARCHAR(100)", "rest": "NOT NULL"},
                {"name": "isbn", "type": "VARCHAR(13)", "rest": "NOT NULL"}
]
import time

def main():
    start = time.time()
    for i in range(2):
        print(generate_row(*intra_table_generator(mock_table)))
    print(time.time() - start)
    
    start = time.time()
    for i in range(2):
        print(generate_row(*intra_table_generator(mock_table2)))
    print(time.time() - start)

if __name__ == "__main__":
    freeze_support()
    main()