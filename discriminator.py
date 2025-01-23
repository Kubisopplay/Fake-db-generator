
from guidance.models import Transformers
from guidance import system, user, assistant, gen, select
from generators import personal, misc
from guidancestuff import loaded_model
#import torch





all_tools = []
all_tools.extend(personal.generators)
all_tools.extend(misc.generators)

tool_descriptions = {}
tool_descriptions.update(personal.generators_dict)
tool_descriptions.update(misc.generators_dict)
print(all_tools)

def make_tool_descriptions():


    descriptions_str = "\n".join([f"{tool}: {tool_descriptions[tool]["description"]}" for tool in tool_descriptions.keys()])
    return descriptions_str
def get_best_tool(field):

    #phi3_lm = Transformers("microsoft/Phi-3-mini-4k-instruct",  echo=False)
    lm = loaded_model
    
    with system():
        lm += f"Your goal is to assign a value generator to a field in a database. The generator is described by its name, and the field is described by its name,\
        type, and additional properties. The generator should be selected based on the field's name, type, and additional properties.\
        The generator should be selected from a list of available generators.\
        Think step by step why would you use a specific generator for a specific field. \
        The generators with their descriptions are: \n {make_tool_descriptions()}"
    with user():
        lm += f"I have a field named {field['name']} of type {field['type']} with additional properties {field['rest']}."
    with assistant():
        lm += f"Thinking about this step by step," + gen("Thoth")
        lm += f"Based on the field's name, type, and additional properties, I think the best generator for this field is" + select(all_tools, "tool") + "."
    #print(lm)
    return lm["tool"]
       
