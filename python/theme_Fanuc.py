from update_themes import *

#************************************  Fanuc Listing language   **************************************
repository = {}
#------------------------------------

repo_begin_end(repository, "!", r'(?=\n)', name_comment, "comment")
repo_begin_end(repository, r'"', r'"', name_string, "string")
repo_begin_end(repository, r'CALL', r';', name_string, "fcn-call")

#match = r'\\b[0-9]\\b'
match = '\\b-?\\d+(\\.\\d*)?([eE][+-]?\\d+)?\\b'
repo_match(repository, match, name_numeric, "numbers")

match = "PROG_SIZE CREATE MODIFIED FILE_NAME VERSION LINE_COUNT MEMORY_SIZE PROTECT TCD DEFAULT_GROUP CONTROL_CODE OWNER COMMENT ATTR "
#match += r"(\/PROG).*\n"
match += "PROG"
repo_match(repository, match, name_control, "control")

match = "MN POS PR DO WAIT DI END"
repo_match(repository, match, name_movements, "movement")

match = "STACK_SIZE TASK_PRIORITY TIME_SLICE BUSY_LAMP_OFF ABORT_REQUEST PAUSE_REQUEST CONFIG"
repo_match(repository, match, name_builtInVar, "built-in-var")

match = "GP1 MESSAGE UTOOL PAUSE UFRAME_NUM UTOOL_NUM"
repo_match(repository, match, name_builtInFcn, "built-in-fcn")

match = r"DATE TIME deg mm FINE UF UT J1 J2 J3 J4 J5 J6 J7 J8 X Y Z W P R READ_WRITE"
repo_match(repository, match, name_builtInTypes, "built-in-types")

match = "[ ]" # &lt;TDN&gt; &lt;DDN&gt; &lt;RDN&gt; &lt;PAR&gt; &lt;ALT&gt; &lt;DIM&gt; &lt;SMT&gt; &lt;VAR&gt; &lt;EIT&gt; &lt;CSE&gt; &lt;EXP&gt; &lt;ARG&gt; &lt;ID&gt; "
repo_match(repository, match, name_operator, "operator")


config_i = dict(default_config)
language_i = {}
language_i["id"] = "Fanuc"
language_i["aliases"]     = "Fanuc LS TP".split(" ")
language_i["extensions"]  = ".LS .ls".split(" ")
language_i["configuration"] = getFileConfig(language_i["id"])
config_i["comments"] = {"lineComment": "!" }
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

    

















