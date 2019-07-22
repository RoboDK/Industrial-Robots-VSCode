from update_themes import *

#************************************  Comau Listing language   **************************************
repository = {}
#------------------------------------

repo_begin_end(repository, "--", r'(?=\n)', name_comment, "comment")
repo_begin_end(repository, r'"', r'"', name_string, "string")
repo_begin_end(repository, r'CALL', r';', name_string, "fcn-call")

#match = r'\\b[0-9]\\b'
#match = '\\b-?\\d+(\\.\\d*)?([eE][+-]?\\d+)?\\b'
match = r'\W\-?\d+(\.\d+)?' #regex for numeric constants
repo_match(repository, match, name_numeric, "numbers")

match = "PROGRAM IMPORT VAR ROUTINE BEGIN END EXPORTED FROM GLOBAL"
match += " REPEAT UNTIL IF THEN ENDIF"
repo_match(repository, match, name_control, "control")


match = "MOVE TO DELAY"
repo_match(repository, match, name_movements, "movement")
match = r"\W\$\w+" # regex $NAME is used for control variables ex $ORNT_TYPE
repo_match(repository, match, name_movements, "movement")

match = "SPD_LIN ON OFF TRUE FALSE RS_WORLD JOINT LINEAR CIRCULAR NOSETTLE FLY_CART FLY_PASS POS"
repo_match(repository, match, name_builtInVar, "built-in-var")

#match = "REPEAT UNTIL IF THEN ENDIF"
#repo_match(repository, match, name_builtInFcn, "built-in-fcn")


#match = r"\W\$\w+" # regex $NAME is used for control variables ex $ORNT_TYPE
#repo_match(repository, match, name_builtInTypes, "built-in-types")


match = "[ ]" # &lt;TDN&gt; &lt;DDN&gt; &lt;RDN&gt; &lt;PAR&gt; &lt;ALT&gt; &lt;DIM&gt; &lt;SMT&gt; &lt;VAR&gt; &lt;EIT&gt; &lt;CSE&gt; &lt;EXP&gt; &lt;ARG&gt; &lt;ID&gt; "
repo_match(repository, match, name_operator, "operator")


config_i = dict(default_config)
language_i = {}
language_i["id"] = "Comau"
language_i["aliases"]     = "Comau pdl".split(" ")
language_i["extensions"]  = ".pdl".split(" ")
language_i["configuration"] = getFileConfig(language_i["id"])
config_i["comments"] = {"lineComment": "--" }
config_i["folding"] = {
        "markers": {
            "start": r'POS',
            "end": r'END'
        }
    }


#Updates the xyntax file
print("Updating syntax...")
update_syntax(language_i["id"], repository)

#Updates the language config file
print("Updating configuration...")
update_config(language_i["id"], config_i)

print("Done")

    

















