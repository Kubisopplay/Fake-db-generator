import re


example = """
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""


def get_fields(sql:str):
    if not sql.strip().startswith("CREATE TABLE"):
        print("Insert a script starting with CREATE TABLE")
        return None
    regex = r"CREATE TABLE (\w+) \((.+)\);"
    lines = re.findall(regex, sql, re.DOTALL)
    if not lines:
        print("Invalid script")
        return None
    fields = []
    table_name = lines[0][0]
    lines = lines[0][1].strip().split("\n")
    for line in lines:
        line = line.split()
        name = line[0]
        line_type = line[1]
        rest = " ".join(line[2:])
        fields.append({
            "name": name,
            "type": line_type,
            "rest": rest
        })
    return{
        "table_name": table_name,
        "fields": fields
    }

        
        

print(get_fields(example))