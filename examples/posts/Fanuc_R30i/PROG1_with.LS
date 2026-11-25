/PROG  PROG1_with
/ATTR
OWNER		= MNEDITOR;
COMMENT		= "RoboDK sequence";
PROG_SIZE	= 0;
CREATE		= DATE 31-12-14  TIME 12:00:00;
MODIFIED	= DATE 31-12-14  TIME 12:00:00;
FILE_NAME	= PROG1_with;
VERSION		= 0;
LINE_COUNT	= 6;
MEMORY_SIZE	= 0;
PROTECT		= READ_WRITE;
TCD:  STACK_SIZE	= 0,
      TASK_PRIORITY	= 50,
      TIME_SLICE	= 0,
      BUSY_LAMP_OFF	= 0,
      ABORT_REQUEST	= 0,
      PAUSE_REQUEST	= 0;
DEFAULT_GROUP	= 1,*,*,*,*,*,*;
CONTROL_CODE	= 00000000 00000000;
/MN
   1:  ! This is a subprogram call to PROG_1 ;
   2:  UFRAME_NUM=1 ;
   3:  ! UF1:0.0,1000.0,0.0,0.0,0.0,0.0 ;
   4:  UTOOL_NUM=1 ;
   5:  ! UT1:0.0,0.0,200.0,0.0,0.0,0.0 ;
   6:J P[1] 20% CNT1 ACC100 ;
/POS
P[1]{
   GP1:
    UF : 1, UT : 1,    
	J1=    -0.000 deg,	J2=    0.000 deg,	J3=    0.000 deg,
	J4=    0.000 deg,	J5=    0.000 deg,	J6=    -0.000 deg
};
/END
