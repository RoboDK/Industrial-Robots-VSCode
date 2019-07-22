from update_themes import *

#************************************  Staubli language   **************************************
repository = {}
#------------------------------------



repo_begin_end(repository, r"//", r'(?=\n)', name_comment, "comment")
repo_begin_end(repository, r'"', r'"', name_string, "string")
repo_begin_end(repository, r'%', r'%', name_string, "fcn-call")

#match = r'\\b[0-9]\\b'
match = '\\b-?\\d+(\\.\\d*)?([eE][+-]?\\d+)?\\b'
repo_match(repository, match, name_numeric, "numbers")

match = "END BEGIN"
repo_match(repository, match, name_control, "control")

match = "movej movel movec"

repo_match(repository, match, name_movements, "movement")

#XML related keywords
match = "xml encoding programs program code Database Datas Data Value Project Parameter Parameters Libraries Library"
#Programming related keywords
match += " nTraj jJoint pPoint flange mNomSpeed true false on off"
repo_match(repository, match, name_builtInVar, "built-in-var")

#xml related keywords
match = "version xmlns xsi name access CDATA key file link alias path"
#Programming related keywords
match += " popUpMsg delay WAIT FOR waitEndMove TIMEOUT stackSize millimeterUnit"
repo_match(repository, match, name_builtInFcn, "built-in-fcn")
match = r'\Wd[oi]\d+' #regex for do#/di# ex do5
repo_match(repository, match, name_builtInFcn, "built-in-fcn")
match = r'\W[a-zA-Z]+\(\)' #regex for void function call ex waitEndMove()
repo_match(repository, match, name_builtInFcn, "built-in-fcn")

match = "x y z rx ry rz shoulder elbow wrist fatherId type size j1 j2 j3 j4 j5 j6 accel vel decel tmax rmax blend leave reach ioLink"
#Looks better as functions to contrast the built in variables
#repo_match(repository, match, name_builtInTypes, "built-in-types")
repo_match(repository, match, name_builtInFcn, "built-in-fcn")

match = "!" # &lt;TDN&gt; &lt;DDN&gt; &lt;RDN&gt; &lt;PAR&gt; &lt;ALT&gt; &lt;DIM&gt; &lt;SMT&gt; &lt;VAR&gt; &lt;EIT&gt; &lt;CSE&gt; &lt;EXP&gt; &lt;ARG&gt; &lt;ID&gt; "
repo_match(repository, match, name_operator, "operator")


config_i = dict(default_config)
language_i = {}
language_i["id"] = "Staubli"
language_i["aliases"]     = "Staubli Scara Stäubli".split(" ")
language_i["extensions"]  = ".pgx .pjx .dtx".split(" ")
language_i["configuration"] = getFileConfig(language_i["id"])
config_i["comments"] = {"lineComment": "//" }
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

    

















