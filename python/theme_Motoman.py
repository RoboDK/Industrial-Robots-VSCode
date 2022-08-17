from update_themes import *

#************************************  YASKAWA INFORM language   **************************************
repository = {}
#------------------------------------



repo_begin_end(repository, "'", r'(?=\n)', name_comment, "comment")
repo_begin_end(repository, r'"', r'"', name_string, "string")
repo_begin_end(repository, r'%', r'%', name_string, "fcn-call")

#match = r'\\b[0-9]\\b'
match = r'\-?\d+(\.\d+)?' #regex for numeric constants
repo_match(repository, match, name_numeric, "numbers")

#Because of the complicated use of / in the header the easy method won't work
#So every word uses a regex
match = r'\/JOB' #regex
repo_match(repository, match, name_control, "control")
match = r'\//NAME' #regex
repo_match(repository, match, name_control, "control")
match = r'\//POS' #regex
repo_match(repository, match, name_control, "control")
match = r'\///NPOS' #regex for ///NPOS configuration
repo_match(repository, match, name_control, "control")
match = r'\///TOOL' #regex
repo_match(repository, match, name_control, "control")
match = r'\///POSTYPE' #regex
repo_match(repository, match, name_control, "control")
match = r'\///PULSE' #regex
repo_match(repository, match, name_control, "control")
match = r'\///RECTAN' #regex
repo_match(repository, match, name_control, "control")
match = r'\///RCONF' #regex
repo_match(repository, match, name_control, "control")
match = r'\//INST' #regex
repo_match(repository, match, name_control, "control")
match = r'\///DATE' #regex
repo_match(repository, match, name_control, "control")
match = r'\///COMM' #regex
repo_match(repository, match, name_control, "control")
match = r'\///ATTR' #regex
repo_match(repository, match, name_control, "control")
match = r'\///GROUP\d+' #regex
repo_match(repository, match, name_control, "control")


match = r'\bP\d{5}' #regex for position use ex P00095
repo_match(repository, match, name_control, "control")
match = r'\b[BE]?C\d{5}' #regex for position constant use ex C00001, BC00001, EC00001
repo_match(repository, match, name_control, "control")


match = "MOVJ MOVL MOVC MOVS IMOV"
repo_match(repository, match, name_movements, "movement")

match = "V VJ"
repo_match(repository, match, name_builtInVar, "built-in-var")
#regex for output ex OT#(5)
match = r'\WOT#\(\d\)'
repo_match(repository, match, name_builtInVar, "built-in-var")
#regex for input IN#(5)
match = r'\WIN#\(\d\)'
repo_match(repository, match, name_builtInVar, "built-in-var")
match = r'\WTL#\(\d\)' #regex for tool number use ex TL#(9)
repo_match(repository, match, name_control, "control")


match = 'NOP SETE SETTOOL TIMER MSG CALL DOUT WAIT PAUSE END' 
repo_match(repository, match, name_builtInFcn, "built-in-fcn")

match = "ON OFF PULSE BASE SC RW RJ RB1"
repo_match(repository, match, name_builtInTypes, "built-in-types")

#match = "OR AND XOR + = - % : ANDIF ORIF NOR"
#repo_match(repository, match, name_operator, "operator")


config_i = dict(default_config)
language_i = {}
language_i["id"] = "Motoman"
language_i["aliases"]     = "Motoman Yaskawa JBI Inform InformII InformIII".split(" ")
language_i["extensions"]  = ".jbi .cnd".split(" ")
language_i["configuration"] = getFileConfig(language_i["id"])
config_i["comments"] = {"lineComment": "'" }
config_i["folding"] = {
        "markers": {
            "start": r'/JOB',
            "end": r'///GROUP'
        }
    }


print("Updating syntax...")
update_syntax(language_i["id"], repository)

print("Updating configuration...")
update_config(language_i["id"], config_i)

print("Done")

    

















