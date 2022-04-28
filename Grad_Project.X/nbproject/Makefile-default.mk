#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Include project Makefile
ifeq "${IGNORE_LOCAL}" "TRUE"
# do not include local makefile. User is passing all local related variables already
else
include Makefile
# Include makefile containing local settings
ifeq "$(wildcard nbproject/Makefile-local-default.mk)" "nbproject/Makefile-local-default.mk"
include nbproject/Makefile-local-default.mk
endif
endif

# Environment
MKDIR=mkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=default
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
IMAGE_TYPE=debug
OUTPUT_SUFFIX=cof
DEBUGGABLE_SUFFIX=cof
FINAL_IMAGE=dist/${CND_CONF}/${IMAGE_TYPE}/Grad_Project.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
else
IMAGE_TYPE=production
OUTPUT_SUFFIX=hex
DEBUGGABLE_SUFFIX=cof
FINAL_IMAGE=dist/${CND_CONF}/${IMAGE_TYPE}/Grad_Project.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
endif

ifeq ($(COMPARE_BUILD), true)
COMPARISON_BUILD=-mafrlcsj
else
COMPARISON_BUILD=
endif

ifdef SUB_IMAGE_ADDRESS
SUB_IMAGE_ADDRESS_COMMAND=--image-address $(SUB_IMAGE_ADDRESS)
else
SUB_IMAGE_ADDRESS_COMMAND=
endif

# Object Directory
OBJECTDIR=build/${CND_CONF}/${IMAGE_TYPE}

# Distribution Directory
DISTDIR=dist/${CND_CONF}/${IMAGE_TYPE}

# Source Files Quoted if spaced
SOURCEFILES_QUOTED_IF_SPACED=/scratch/team-2a/Desktop/Grad_Driver_Files/crc16.c /scratch/team-2a/Desktop/Grad_Driver_Files/joystick.c /scratch/team-2a/Desktop/Grad_Driver_Files/motor.c /scratch/team-2a/Desktop/Grad_Driver_Files/timer.c /scratch/team-2a/Desktop/Grad_Driver_Files/touch.c /scratch/team-2a/Desktop/Grad_Driver_Files/uart.c /scratch/team-2a/Desktop/Grad_Driver_Files/main.c

# Object Files Quoted if spaced
OBJECTFILES_QUOTED_IF_SPACED=${OBJECTDIR}/_ext/984345814/crc16.o ${OBJECTDIR}/_ext/984345814/joystick.o ${OBJECTDIR}/_ext/984345814/motor.o ${OBJECTDIR}/_ext/984345814/timer.o ${OBJECTDIR}/_ext/984345814/touch.o ${OBJECTDIR}/_ext/984345814/uart.o ${OBJECTDIR}/_ext/984345814/main.o
POSSIBLE_DEPFILES=${OBJECTDIR}/_ext/984345814/crc16.o.d ${OBJECTDIR}/_ext/984345814/joystick.o.d ${OBJECTDIR}/_ext/984345814/motor.o.d ${OBJECTDIR}/_ext/984345814/timer.o.d ${OBJECTDIR}/_ext/984345814/touch.o.d ${OBJECTDIR}/_ext/984345814/uart.o.d ${OBJECTDIR}/_ext/984345814/main.o.d

# Object Files
OBJECTFILES=${OBJECTDIR}/_ext/984345814/crc16.o ${OBJECTDIR}/_ext/984345814/joystick.o ${OBJECTDIR}/_ext/984345814/motor.o ${OBJECTDIR}/_ext/984345814/timer.o ${OBJECTDIR}/_ext/984345814/touch.o ${OBJECTDIR}/_ext/984345814/uart.o ${OBJECTDIR}/_ext/984345814/main.o

# Source Files
SOURCEFILES=/scratch/team-2a/Desktop/Grad_Driver_Files/crc16.c /scratch/team-2a/Desktop/Grad_Driver_Files/joystick.c /scratch/team-2a/Desktop/Grad_Driver_Files/motor.c /scratch/team-2a/Desktop/Grad_Driver_Files/timer.c /scratch/team-2a/Desktop/Grad_Driver_Files/touch.c /scratch/team-2a/Desktop/Grad_Driver_Files/uart.c /scratch/team-2a/Desktop/Grad_Driver_Files/main.c



CFLAGS=
ASFLAGS=
LDLIBSOPTIONS=

############# Tool locations ##########################################
# If you copy a project from one host to another, the path where the  #
# compiler is installed may be different.                             #
# If you open this project with MPLAB X in the new host, this         #
# makefile will be regenerated and the paths will be corrected.       #
#######################################################################
# fixDeps replaces a bunch of sed/cat/printf statements that slow down the build
FIXDEPS=fixDeps

.build-conf:  ${BUILD_SUBPROJECTS}
ifneq ($(INFORMATION_MESSAGE), )
	@echo $(INFORMATION_MESSAGE)
endif
	${MAKE}  -f nbproject/Makefile-default.mk dist/${CND_CONF}/${IMAGE_TYPE}/Grad_Project.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}

MP_PROCESSOR_OPTION=33FJ256MC710
MP_LINKER_FILE_OPTION=,--script=p33FJ256MC710.gld
# ------------------------------------------------------------------------------------
# Rules for buildStep: compile
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${OBJECTDIR}/_ext/984345814/crc16.o: /scratch/team-2a/Desktop/Grad_Driver_Files/crc16.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/crc16.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/crc16.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/crc16.c  -o ${OBJECTDIR}/_ext/984345814/crc16.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/crc16.o.d"      -g -D__DEBUG -D__MPLAB_DEBUGGER_ICD3=1    -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/crc16.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/_ext/984345814/joystick.o: /scratch/team-2a/Desktop/Grad_Driver_Files/joystick.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/joystick.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/joystick.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/joystick.c  -o ${OBJECTDIR}/_ext/984345814/joystick.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/joystick.o.d"      -g -D__DEBUG -D__MPLAB_DEBUGGER_ICD3=1    -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/joystick.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/_ext/984345814/motor.o: /scratch/team-2a/Desktop/Grad_Driver_Files/motor.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/motor.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/motor.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/motor.c  -o ${OBJECTDIR}/_ext/984345814/motor.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/motor.o.d"      -g -D__DEBUG -D__MPLAB_DEBUGGER_ICD3=1    -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/motor.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/_ext/984345814/timer.o: /scratch/team-2a/Desktop/Grad_Driver_Files/timer.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/timer.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/timer.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/timer.c  -o ${OBJECTDIR}/_ext/984345814/timer.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/timer.o.d"      -g -D__DEBUG -D__MPLAB_DEBUGGER_ICD3=1    -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/timer.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/_ext/984345814/touch.o: /scratch/team-2a/Desktop/Grad_Driver_Files/touch.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/touch.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/touch.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/touch.c  -o ${OBJECTDIR}/_ext/984345814/touch.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/touch.o.d"      -g -D__DEBUG -D__MPLAB_DEBUGGER_ICD3=1    -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/touch.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/_ext/984345814/uart.o: /scratch/team-2a/Desktop/Grad_Driver_Files/uart.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/uart.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/uart.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/uart.c  -o ${OBJECTDIR}/_ext/984345814/uart.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/uart.o.d"      -g -D__DEBUG -D__MPLAB_DEBUGGER_ICD3=1    -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/uart.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/_ext/984345814/main.o: /scratch/team-2a/Desktop/Grad_Driver_Files/main.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/main.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/main.c  -o ${OBJECTDIR}/_ext/984345814/main.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/main.o.d"      -g -D__DEBUG -D__MPLAB_DEBUGGER_ICD3=1    -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/main.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
else
${OBJECTDIR}/_ext/984345814/crc16.o: /scratch/team-2a/Desktop/Grad_Driver_Files/crc16.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/crc16.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/crc16.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/crc16.c  -o ${OBJECTDIR}/_ext/984345814/crc16.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/crc16.o.d"        -g -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/crc16.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/_ext/984345814/joystick.o: /scratch/team-2a/Desktop/Grad_Driver_Files/joystick.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/joystick.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/joystick.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/joystick.c  -o ${OBJECTDIR}/_ext/984345814/joystick.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/joystick.o.d"        -g -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/joystick.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/_ext/984345814/motor.o: /scratch/team-2a/Desktop/Grad_Driver_Files/motor.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/motor.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/motor.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/motor.c  -o ${OBJECTDIR}/_ext/984345814/motor.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/motor.o.d"        -g -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/motor.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/_ext/984345814/timer.o: /scratch/team-2a/Desktop/Grad_Driver_Files/timer.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/timer.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/timer.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/timer.c  -o ${OBJECTDIR}/_ext/984345814/timer.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/timer.o.d"        -g -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/timer.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/_ext/984345814/touch.o: /scratch/team-2a/Desktop/Grad_Driver_Files/touch.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/touch.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/touch.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/touch.c  -o ${OBJECTDIR}/_ext/984345814/touch.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/touch.o.d"        -g -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/touch.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/_ext/984345814/uart.o: /scratch/team-2a/Desktop/Grad_Driver_Files/uart.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/uart.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/uart.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/uart.c  -o ${OBJECTDIR}/_ext/984345814/uart.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/uart.o.d"        -g -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/uart.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/_ext/984345814/main.o: /scratch/team-2a/Desktop/Grad_Driver_Files/main.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/984345814" 
	@${RM} ${OBJECTDIR}/_ext/984345814/main.o.d 
	@${RM} ${OBJECTDIR}/_ext/984345814/main.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  /scratch/team-2a/Desktop/Grad_Driver_Files/main.c  -o ${OBJECTDIR}/_ext/984345814/main.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/_ext/984345814/main.o.d"        -g -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp=${DFP_DIR}/xc16
	@${FIXDEPS} "${OBJECTDIR}/_ext/984345814/main.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: assemble
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: assemblePreproc
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: link
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
dist/${CND_CONF}/${IMAGE_TYPE}/Grad_Project.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk  /scratch/team-2a/Desktop/Grad_Driver_Files/lcd.a  
	@${MKDIR} dist/${CND_CONF}/${IMAGE_TYPE} 
	${MP_CC} $(MP_EXTRA_LD_PRE)  -o dist/${CND_CONF}/${IMAGE_TYPE}/Grad_Project.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}  ${OBJECTFILES_QUOTED_IF_SPACED}    /scratch/team-2a/Desktop/Grad_Driver_Files/lcd.a  -mcpu=$(MP_PROCESSOR_OPTION)        -D__DEBUG=__DEBUG -D__MPLAB_DEBUGGER_ICD3=1  -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)   -mreserve=data@0x800:0x81F -mreserve=data@0x820:0x821 -mreserve=data@0x822:0x823 -mreserve=data@0x824:0x825 -mreserve=data@0x826:0x84F   -Wl,,,--defsym=__MPLAB_BUILD=1,--defsym=__MPLAB_DEBUG=1,--defsym=__DEBUG=1,-D__DEBUG=__DEBUG,--defsym=__MPLAB_DEBUGGER_ICD3=1,$(MP_LINKER_FILE_OPTION),--stack=16,--check-sections,--data-init,--pack-data,--handles,--isr,--no-gc-sections,--fill-upper=0,--stackguard=16,--no-force-link,--smart-io,-Map="${DISTDIR}/${PROJECTNAME}.${IMAGE_TYPE}.map",--report-mem,--memorysummary,dist/${CND_CONF}/${IMAGE_TYPE}/memoryfile.xml$(MP_EXTRA_LD_POST)  -mdfp=${DFP_DIR}/xc16 
	
else
dist/${CND_CONF}/${IMAGE_TYPE}/Grad_Project.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk  /scratch/team-2a/Desktop/Grad_Driver_Files/lcd.a 
	@${MKDIR} dist/${CND_CONF}/${IMAGE_TYPE} 
	${MP_CC} $(MP_EXTRA_LD_PRE)  -o dist/${CND_CONF}/${IMAGE_TYPE}/Grad_Project.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}  ${OBJECTFILES_QUOTED_IF_SPACED}    /scratch/team-2a/Desktop/Grad_Driver_Files/lcd.a  -mcpu=$(MP_PROCESSOR_OPTION)        -omf=coff -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -Wl,,,--defsym=__MPLAB_BUILD=1,$(MP_LINKER_FILE_OPTION),--stack=16,--check-sections,--data-init,--pack-data,--handles,--isr,--no-gc-sections,--fill-upper=0,--stackguard=16,--no-force-link,--smart-io,-Map="${DISTDIR}/${PROJECTNAME}.${IMAGE_TYPE}.map",--report-mem,--memorysummary,dist/${CND_CONF}/${IMAGE_TYPE}/memoryfile.xml$(MP_EXTRA_LD_POST)  -mdfp=${DFP_DIR}/xc16 
	${MP_CC_DIR}/xc16-bin2hex dist/${CND_CONF}/${IMAGE_TYPE}/Grad_Project.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX} -a  -omf=coff   -mdfp=${DFP_DIR}/xc16 
	
endif


# Subprojects
.build-subprojects:


# Subprojects
.clean-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r build/default
	${RM} -r dist/default

# Enable dependency checking
.dep.inc: .depcheck-impl

DEPFILES=$(shell "${PATH_TO_IDE_BIN}"mplabwildcard ${POSSIBLE_DEPFILES})
ifneq (${DEPFILES},)
include ${DEPFILES}
endif
