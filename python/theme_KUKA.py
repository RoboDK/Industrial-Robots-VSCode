from update_themes import *

#************************************  KUKA language   **************************************
repository = {}
#------------------------------------

repository_i = {}
match_type = "control"
match = "REPEAT FOR WHILE LOOP DEF IF THEN ELSE SWITCH LOOP"
match += " UNTIL ENDFOR ENDWHILE ENDLOOP END ENDIF ENDSWITCH ENDLOOP"
match += " DEF INI END ENDFCT ENDDAT WAIT GOTO CASE DEFAULT DEFFCT ENDFCT"
match += " DEFDAT PUBLIC ENDDAT RETURN EXIT HALT"
match += " INTERRUPT WHEN DO BRAKE RESUME ENABLE DISABLE"
repository_i['match'] = match.upper() + " " + match.lower()
repository_i['name'] = name_control
repository[match_type] = repository_i

repository_i = {}
match_type = "movement"



match = "PTP LIN CIRC SPTP SLIN"
repository_i['match'] = match.upper() + " " + match.lower()
repository_i['name'] = name_movements
repository[match_type] = repository_i

repository_i = {}
match_type = "built-in-fcn"
match = "BAS SET_KRLMSG EXISTS_KRLMSG CLEAR_KRLMSG TRIGGER DISTANCE SET_KRLDLG EXISTS_KRLDLG"
repository_i['match'] = match.upper() + " " + match.lower()
repository_i['name'] = name_builtInFcn
repository[match_type] = repository_i

repository_i = {}
match_type = "built-in-types"
match = "DECL GLOBAL CONST INT REAL BOOL CHAR PRIO FRAME POS E6POS AXIS E6AXIS"
repository_i['match'] = match.upper() + " " + match.lower()
repository_i['name'] = name_builtInTypes
repository[match_type] = repository_i

repository_i = {}
match_type = "built-in-var"
match = "BASE_DATA TOOL_DATA $ADVANCE $TOOL $BASE $AXIS_ACT $ACT_EX_AX EX_AX_DATA"
match += " #INITMOV BWDSTART"
match += " ANOUT OUT IN ANIN ON OFF TRUE FALSE"
match += " $ACC $VEL $APO C_DIS C_PTP"
match += " $TIMER_STOP $TIMER_FLAG $TIMER"
repository_i['match'] = match.upper() + " " + match.lower()
repository_i['name'] = name_builtInVar
repository[match_type] = repository_i

repository_i = {}
match_type = "operator"
match = "= &lt; &gt; + - , ( ) { } [ ]"
repository_i['match'] = match.upper() + " " + match.lower()
repository_i['name'] = name_operator
repository[match_type] = repository_i


config_i = dict(default_config)
language_i = {}
language_i["id"] = "KUKA KRC"
language_i["aliases"]     = "KUKA KRC2 KRC4 SRC DAT".split(" ")
language_i["extensions"]  = ".src .dat".split(" ")
language_i["configuration"] = getFileConfig(language_i["id"])
config_i["comments"] = {"lineComment": ";" }
config_i["folding"] = {
        "markers": {
            "start": "^\\\\s*;FOLD",
            "end": "^\\\\s*;ENDFOLD"
        }
    }



print("Updating syntax...")
update_syntax(language_i["id"], repository)

print("Updating configuration...")
update_config(language_i["id"], config_i)

print("Done")

    
