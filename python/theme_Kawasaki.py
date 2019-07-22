from update_themes import *

#************************************  kawasaki language   **************************************
repository = {}
#------------------------------------



repo_begin_end(repository, ";", r'(?=\n)', name_comment, "comment")
repo_begin_end(repository, r'"', r'"', name_string, "string")
repo_begin_end(repository, r'%', r'%', name_string, "fcn-call")

#match = r'\\b[0-9]\\b'
match = '\\b-?\\d+(\\.\\d*)?([eE][+-]?\\d+)?\\b'
repo_match(repository, match, name_numeric, "numbers")

match = r'\.PROGRAM' #regex for .PROGRAM
repo_match(repository, match, name_control, "control")
match = r'\.END' #regex for .END
repo_match(repository, match, name_control, "control")


match = "TRANS C1MOVE C2MOVE"
repo_match(repository, match, name_movements, "movement")

match = "SPEED ACCEL"
repo_match(repository, match, name_builtInVar, "built-in-var")

match = "BASE JMOVE LMOVE CALL ALWAYS NEVER"
repo_match(repository, match, name_builtInFcn, "built-in-fcn")


match = r'\WMM\/S' #regex for mm/s
repo_match(repository, match, name_builtInTypes, "built-in-types")
match = r"TYPE TWAIT SIGNAL WAIT SIG TOOL"
repo_match(repository, match, name_builtInTypes, "built-in-types")


match = "< >" # &lt;TDN&gt; &lt;DDN&gt; &lt;RDN&gt; &lt;PAR&gt; &lt;ALT&gt; &lt;DIM&gt; &lt;SMT&gt; &lt;VAR&gt; &lt;EIT&gt; &lt;CSE&gt; &lt;EXP&gt; &lt;ARG&gt; &lt;ID&gt; "
repo_match(repository, match, name_operator, "operator")


config_i = dict(default_config)
language_i = {}
language_i["id"] = "Kawasaki"
language_i["aliases"]     = "Kawasaki".split(" ")
language_i["extensions"]  = ".pg".split(" ")
language_i["configuration"] = getFileConfig(language_i["id"])
config_i["comments"] = {"lineComment": ";" }
config_i["folding"] = {
        "markers": {
            "start": r'%%%',
            "end": r'%%%'
        }
    }


print("Updating syntax...")
update_syntax(language_i["id"], repository)

print("Updating configuration...")
update_config(language_i["id"], config_i)

print("Done")

    

















