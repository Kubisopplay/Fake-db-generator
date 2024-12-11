


generators_dict ={
    "id_generator": {"description": "Generates a unique id, starting from 0", "constraints": []}
}

generators = generators_dict.keys()

last_id = -1

def id_generator():
    global last_id
    last_id += 1
    return last_id 

def reset_id():
    global last_id
    last_id = -1
    
