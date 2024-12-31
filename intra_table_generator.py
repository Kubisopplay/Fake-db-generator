

from generators.personal import generators_dict as personal_generators_dict
from generators.misc import generators_dict as misc_generators_dict
from guidance import system, user, assistant, gen, select
from guidancestuff import loaded_model
from generators import personal, misc
from discriminator import get_best_tool

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
        
        
def generate_row(primary_constraints, intermediate_constraints, all_generators, generators_ordered):
    primary_generator = loaded_model + "Create a value for a constraint for a set of generators"
    constraints = {}
    for constraint in primary_constraints:
        generator = primary_generator + "\r\nName of the generator: " + constraint
        generator += "\r\n The value that is gonna define the row of the generator is: " + gen("value", temperature=0.9, max_tokens=20)
        constraints[constraint] = generator["value"]
    
    for generator in intermediate_constraints:
        generator_constraints = all_generators[generator]
        temp = {}
        for constraint in generator_constraints:
            temp[constraint] = constraints[constraint]
        constraints[generator] = all_generators[generator]["function"](**temp)
    
mock_table = [{"name": "id", "type": "INT", "rest": "PRIMARY KEY"},
                {"name": "name", "type": "VARCHAR(100)", "rest": "NOT NULL"},
                {"name": "surname", "type": "VARCHAR(510)", "rest": "NOT NULL"},
                {"name": "email", "type": "VARCHAR(100)", "rest": "NOT NULL"}]


print(intra_table_generator(mock_table))
