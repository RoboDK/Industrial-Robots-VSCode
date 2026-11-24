from update_themes import *

#************************************  Fanuc Listing language   **************************************
repository = {}
#------------------------------------

repo_begin_end(repository, r'(?<!IF.*)!', r'(?=\n)', name_comment, "comment")
repo_begin_end(repository, r'"', r'"', name_string, "string")
repo_begin_end(repository, r'CALL', r';', name_string, "fcn-call")

#match = r'\\b[0-9]\\b'
#match = '\\b-?\\d+(\\.\\d*)?([eE][+-]?\\d+)?\\b'
match = r'\-?\d+\.\d+' #regex for numeric constants
repo_match(repository, match, name_numeric, "numbers")

match = "PROG_SIZE CREATE MODIFIED FILE_NAME VERSION LINE_COUNT MEMORY_SIZE PROTECT TCD DEFAULT_GROUP CONTROL_CODE OWNER COMMENT"
repo_match(repository, match, name_control, "control")
match = r'\bLBL\[\d+\]' #regex for labels ex LBL[1] (before the keyword list so the full token wins)
repo_match(repository, match, name_control, "control")
match = "IF THEN ELSE ENDIF JMP LBL FOR ENDFOR SELECT RUN ABORT AND OR NOT"
repo_match(repository, match, name_control, "control")
match = r'\s\d+:' #regex for line count ex 1:
repo_match(repository, match, name_control, "control")
match = r'\/PROG' #regex for /PROG
repo_match(repository, match, name_control, "control")
match = r'\/ATTR' #regex for /ATTR
repo_match(repository, match, name_control, "control")
match = r'\/MN' #regex for /MN
repo_match(repository, match, name_control, "control")
match = r'\/POS' #regex for /POS
repo_match(repository, match, name_control, "control")
match = r'\/END' #regex for /END
repo_match(repository, match, name_control, "control")
#More of a built-in type but looks better as control
match = r'\d+mm/sec' #regex for NUMmm/s
repo_match(repository, match, name_control, "control")
match = r'\d+%' #regex for joint speed ex 50%
repo_match(repository, match, name_control, "control")


# Specific patterns go before the keyword list: when two rules match at the
# same position TextMate keeps the first one, so DO[10] must come before DO
match = r'\bD[OI]\[\d+\]' #regex for DI and DO ex DO[1], DI[101]
repo_match(repository, match, name_movements, "movement")
match = "MN POS WAIT DI END"
repo_match(repository, match, name_movements, "movement")


match = "STACK_SIZE TASK_PRIORITY TIME_SLICE BUSY_LAMP_OFF ABORT_REQUEST PAUSE_REQUEST CONFIG"
repo_match(repository, match, name_builtInVar, "built-in-var")
match = r'\b(R|AR|SR|GI|GO|AI|AO|RI|RO|UI|UO|SI|SO|F|TIMER)\[\d+\]' #regex for registers and I/O ex R[1], TIMER[2]
repo_match(repository, match, name_builtInVar, "built-in-var")

match = r'\bMESSAGE\[[^\]]*\]' #regex for MESSAGE command
repo_match(repository, match, name_builtInFcn, "built-in-fcn")
match = r'\bUTOOL\[\d+\]' #regex for UTOOL configuration
repo_match(repository, match, name_builtInFcn, "built-in-fcn")
match = r'\bUFRAME\[\d+\]' #regex for UFRAME configuration
repo_match(repository, match, name_builtInFcn, "built-in-fcn")
match = "GP1 MESSAGE UFRAME UTOOL PAUSE UFRAME_NUM UTOOL_NUM"
repo_match(repository, match, name_builtInFcn, "built-in-fcn")


match = r'\bCNT\d+' #regex for continuous termination ex CNT50
repo_match(repository, match, name_builtInTypes, "built-in-types")
match = "DATE TIME deg mm FINE UF UT J1 J2 J3 J4 J5 J6 J7 J8 X Y Z W R READ_WRITE ON OFF"
repo_match(repository, match, name_builtInTypes, "built-in-types")
match = r'\b[LJ][\s]P\[\d+\]' #regex for linear and joint movement
repo_match(repository, match, name_builtInTypes, "built-in-types")
match = r'\bPR\[\d+,\d+\]' #regex for position register element ex PR[9,1]
repo_match(repository, match, name_builtInTypes, "built-in-types")
match = r'\bPR?\[\d+\]' #regex for position or position register ex P[4], PR[9]
repo_match(repository, match, name_builtInTypes, "built-in-types")


match = r'\<>|<=|>=|[-+*/=<>]' #regex for operators
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

    

















