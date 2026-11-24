from update_themes import *

#URScript: a Python-like language used by Universal Robots controllers
#************************************  Universal robots Listing language   **************************************
repository = {}
#------------------------------------

repo_begin_end(repository, "#", r'(?=\n)', name_comment, "comment")
repo_begin_end(repository, r'"', r'"', name_string, "string")

#match = r'\\b[0-9]\\b'
#match = '\\b-?\\d+(\\.\\d*)?([eE][+-]?\\d+)?\\b'
match = r'\-?(?<![\w.])\d+(\.\d+)?\b' #regex for numeric constants (not digits inside identifiers)
repo_match(repository, match, name_numeric, "numbers")

match = "if elif else end def sec thread while return run kill halt break continue and or not"
repo_match(repository, match, name_control, "control")


match = "movej movel movec movep servoj servoc speedj speedl stopj stopl popup sleep sync"
repo_match(repository, match, name_movements, "movement")
#match = r"\W\$\w+" # regex $NAME is used for control variables ex $ORNT_TYPE
#repo_match(repository, match, name_movements, "movement")

match = "global local True False None"
repo_match(repository, match, name_builtInVar, "built-in-var")
match = r'\p\[(-?\d+\.?\d+?,?\s?)+\]' #regex for xyzwpr position
repo_match(repository, match, name_builtInVar, "built-in-var")

match = "set_tcp set_payload set_gravity get_actual_joint_positions get_actual_tcp_pose get_target_joint_positions get_target_tcp_pose get_inverse_kin get_forward_kin pose_trans pose_inv pose_add pose_sub pose_dist"
match += " set_digital_out get_digital_in get_digital_out set_analog_out get_analog_in set_tool_digital_out get_tool_digital_in set_tool_voltage set_configurable_digital_out get_configurable_digital_in"
match += " set_standard_digital_out get_standard_digital_in get_standard_digital_out set_standard_analog_out get_standard_analog_in"
match += " textmsg str_cat to_str to_num socket_open socket_close socket_send_string socket_send_line socket_send_int socket_read_string socket_read_ascii_float socket_read_binary_integer socket_set_var socket_get_var"
match += " force_mode end_force_mode freedrive_mode end_freedrive_mode zero_ftsensor get_tcp_force rpc_factory"
match += " sin cos tan asin acos atan atan2 sqrt pow log exp floor ceil abs norm d2r r2d"
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
            "start": r'^\s*(def|thread|if|while)\b',
            "end": r'^\s*end\b'
        }
    }


#Updates the xyntax file
print("Updating syntax...")
update_syntax(language_i["id"], repository)

#Updates the language config file
print("Updating configuration...")
update_config(language_i["id"], config_i)

print("Done")
