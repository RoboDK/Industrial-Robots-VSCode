from update_themes import *

#************************************  ABB RAPID language   **************************************
repository = {}
#------------------------------------



repo_begin_end(repository, "'", r'(?=\n)', name_comment, "comment")
repo_begin_end(repository, r'"', r'"', name_string, "string")
repo_begin_end(repository, r'%', r'%', name_string, "fcn-call")

match = r'\\b[0-9]\\b'
repo_match(repository, match, name_numeric, "numbers")

match = "IF UNTIL ENWAIT ELSE ELSEIF FOR ENDFOR IFTHEN ENDIF RET SWITCH WHILE ENDWHILE JUMP CALL TIMER PAUSE CWAIT MSG ADVINIT ADVSTOP PRINT CLS ABORT SETUALM DIALOG DIALSB"
repo_match(repository, match, name_control, "control")

match = "MOVJ MOVL MOVC MOVS IMOV"
repo_match(repository, match, name_movements, "movement")

match = "OFF ON TOOL"
match += " IN# OUT# TL# OG# IG# OT# IARG#"
match += " DIN DOUT WAIT PULSE AOUT ARATION ARATIOF ANTOUT"
repo_match(repository, match, name_builtInVar, "built-in-var")

match = "SPEED REFP PL FPT"
match += " CLEAR INC DEC SET ADD SUB MUL DIV CNVRT NOT XOR MFRAME SETE GETE GETS SQRT SIN COS ATAN MULMAT INVMAT SETFILE GETFILE SETREG GETREG GETARG GETTOOL SETTOOL JOB SFTON SFTOF MSHIFT GETPOS INV"
repo_match(repository, match, name_builtInFcn, "built-in-fcn")

match = ""
repo_match(repository, match, name_builtInTypes, "built-in-types")

match = "OR AND XOR + = - % : ANDIF ORIF NOR"
repo_match(repository, match, name_operator, "operator")


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

    

















