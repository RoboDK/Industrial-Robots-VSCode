from update_themes import *

#Mostly just python,
#You can add the file assosiation in the users settings.json or 
#just copy paste the one in this directory over the old one.
#You can find your settings.json in the following locations
#Windows %APPDATA%\Code\User\settings.json
#macOS $HOME/Library/Application Support/Code/User/settings.json
#Linux $HOME/.config/Code/User/settings.json
#This file just adds the keywords python is missing for now
#************************************  Universal robots Listing language   **************************************
repository = {}
#------------------------------------

repo_begin_end(repository, "#", r'(?=\n)', name_comment, "comment")
repo_begin_end(repository, r'"', r'"', name_string, "string")
repo_begin_end(repository, r'CALL', r';', name_string, "fcn-call")

#match = r'\\b[0-9]\\b'
#match = '\\b-?\\d+(\\.\\d*)?([eE][+-]?\\d+)?\\b'
match = r'\-?\d+(\.\d+)?' #regex for numeric constants
repo_match(repository, match, name_numeric, "numbers")

match = "if else end def while"
repo_match(repository, match, name_control, "control")


match = "movej movel movec popup sleep"
repo_match(repository, match, name_movements, "movement")
#match = r"\W\$\w+" # regex $NAME is used for control variables ex $ORNT_TYPE
#repo_match(repository, match, name_movements, "movement")

match = "global TRUE FALSE"
repo_match(repository, match, name_builtInVar, "built-in-var")
match = r'\p\[(-?\d+\.?\d+?,?\s?)+\]' #regex for xyzwpr position
repo_match(repository, match, name_builtInVar, "built-in-var")

match = "set_standard_digital_out get_standard_digital_in sync set_tcp"
repo_match(repository, match, name_builtInFcn, "built-in-fcn")


match = "speed_ms speed_rads accel_mss accel_radss blend_radius_m blocking"
#It looks nicer under built-in-fcn as these control hardware even though they are built in variables
#repo_match(repository, match, name_builtInVar, "built-in-var")
repo_match(repository, match, name_builtInFcn, "built-in-fcn")

#match = "[ ]" # &lt;TDN&gt; &lt;DDN&gt; &lt;RDN&gt; &lt;PAR&gt; &lt;ALT&gt; &lt;DIM&gt; &lt;SMT&gt; &lt;VAR&gt; &lt;EIT&gt; &lt;CSE&gt; &lt;EXP&gt; &lt;ARG&gt; &lt;ID&gt; "
#repo_match(repository, match, name_operator, "operator")


config_i = dict(default_config)
language_i = {}
language_i["id"] = "universal_robots"
language_i["aliases"]     = "Universal_Robots".split(" ")
language_i["extensions"]  = ".script".split(" ")
language_i["configuration"] = getFileConfig(language_i["id"])
config_i["comments"] = {"lineComment": "#" }
config_i["folding"] = {
        "markers": {
            "start": r'def',
            "end": r'end'
        }
    }


#Updates the xyntax file
print("Updating syntax...")
update_syntax(language_i["id"], repository)

#Updates the language config file
print("Updating configuration...")
update_config(language_i["id"], config_i)

print("Done")
