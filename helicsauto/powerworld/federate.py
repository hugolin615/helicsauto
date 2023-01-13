#!/usr/bin/env python
# coding: utf-8
 
 
import win32com.client
from win32com.client import VARIANT
import numpy as np
import pythoncom
 
 
def CheckResultForError(SimAutoOutput, Message):
    if SimAutoOutput[0] != '':
        print ('Error: ' + SimAutoOutput[0])
        return False
    else:
        print (Message)
        return True
 
# The following will open the connection
simauto_obj = win32com.client.Dispatch("pwrworld.SimulatorAuto")
print(simauto_obj)
 
pwbfile = 'C:\\Users\\decps\\Documents\\Experiments\\220313_FaultDetectionEnhancement\\IEEE9Bus\\WSCC9bus.pwb'
print(f'{pwbfile}')
 
if not CheckResultForError(simauto_obj.OpenCase(pwbfile), 'Open Case'):
    print('here')
    del simauto_obj
# print(f'type of OUtput: {type(SimAutoOutput)}, {SimAutoOutput}, {SimAutoOutput[0]}')
# type of OUtput: <class 'tuple'>, ('',),
# The following will close the connection
 
# Set script command to cause Simulator to enter Run Mode
scriptcommand = 'EnterMode(RUN)'
 
# Make the RunScriptCommand call
if not CheckResultForError(simauto_obj.RunScriptCommand(scriptcommand), f'{scriptcommand}'):
    del simauto_obj
 
# Set script command to cause Simulator to perform a single, standard solution
scriptcommand = 'SolvePowerFlow(RECTNEWT)'
 
# Make the RunScriptCommand call
if not CheckResultForError(simauto_obj.RunScriptCommand(scriptcommand), f'{scriptcommand}'):
    del simauto_obj
 
# Test Getting Parameters
busparamlist = ['BusNum', 'BusPUVolt', 'BusAngle']
loadparamlist = ['BusNum', 'LoadID', 'LoadMW', 'LoadMVR']
 
SimAutoOutput = simauto_obj.GetParametersMultipleElement('LOAD', loadparamlist, '')
if not CheckResultForError(SimAutoOutput, 'GetParameters'):
    del simauto_obj
 
print(f'type of OUtput: {type(SimAutoOutput)}, {SimAutoOutput}')
print(f'{type(SimAutoOutput[1][1])},{SimAutoOutput[1][1]}')
 
loadResult = SimAutoOutput[1]
 
val_busnum = loadResult[0];
val_id = loadResult[1];
val_loadmw = loadResult[2];
val_loadmvr = loadResult[3];
val_busnum_np = np.array(list(map(float, val_busnum)))
val_id_np = np.array(list(map(float, val_id)))
val_loadmw_np = np.array(list(map(float, val_loadmw)))
val_loadmvr_np = np.array(list(map(float, val_loadmvr)))
num_obj = len(val_busnum)
n_attr = len(loadparamlist)
print(f'val_busnum: {val_busnum}')
print(f'val_id: {val_id}')
print(f'val_loadmw: {val_loadmw}')
print(f'val_loadmvr: {val_loadmvr}')
print(f'len(loadparamlist)')
print(f'num_obj: {num_obj}; n_attr: {n_attr}')
 
 
## HELICSAUTO: Register
import helics as h
fed = h.helicsCreateValueFederateFromConfig('../powerworld/fed_config.json')
 
## HELICSAUTO: Execute
h.helicsFederateEnterExecutingMode(fed)
hours = 1
total_interval = int(60 * 60 * hours)
update_interval = int(h.helicsFederateGetTimeProperty(fed, h.HELICS_PROPERTY_TIME_PERIOD))
grantedtime = 0
while grantedtime < total_interval:
 
    scriptcommand = 'EnterMode(EDIT);'
    if not CheckResultForError(simauto_obj.RunScriptCommand(scriptcommand), f'{scriptcommand}'):
        del simauto_obj
 
    #print(f'{val_loadmw_np}')
    #val_loadmw_np2 = np.multiply(val_loadmw_np, np.array([0.9, 0.8, 0.7]))
    #val_loadmvr_np2 = np.multiply(val_loadmvr_np, np.array([1.1, 1.2, 1.3]))
    #val_mat = np.array([val_busnum_np, val_id_np, val_loadmw_np2, val_loadmvr_np2])
    #val_list = np.reshape(val_mat, num_obj * n_attr)
    #val_list = val_list.tolist()
    #val_tuple = tuple(val_list)
 
    ## HELICSAUTO: Sync
    requested_time = grantedtime + update_interval
    grantedtime = h.helicsFederateRequestTime(fed, requested_time)
 
    feeder_var = complex(0, 0)
    ## HELICSAUTO: Subscribe, feeder_var, complex, Feeder_S 
    subid = h.helicsFederateGetSubscription(fed, 'Feeder_S ')
    feeder_var = h.helicsInputGetComplex((subid))
 
    FieldArray = VARIANT(pythoncom.VT_VARIANT | pythoncom.VT_ARRAY, loadparamlist)
    AllValueArray = [None]*num_obj
    AllValueArray[0] = VARIANT(pythoncom.VT_VARIANT | pythoncom.VT_ARRAY, [5, 1, val_loadmw_np[0] + feeder_var, val_loadmvr_np[0]])
    AllValueArray[1] = VARIANT(pythoncom.VT_VARIANT | pythoncom.VT_ARRAY, [6, 1, val_loadmw_np[1], val_loadmvr_np[1]])
    AllValueArray[2] = VARIANT(pythoncom.VT_VARIANT | pythoncom.VT_ARRAY, [8, 1, val_loadmw_np[2], val_loadmvr_np[2]])
    #SimAutoOutput = simauto_obj.ChangeParametersMultipleElementFlatInput('LOAD', loadparamlist, num_obj, val_tuple)
    if not CheckResultForError(simauto_obj.ChangeParametersMultipleElement("LOAD", FieldArray, AllValueArray), 'Change Parameter'):
        del simauto_obj
 
    scriptcommand = 'EnterMode(RUN)'
    if not CheckResultForError(simauto_obj.RunScriptCommand(scriptcommand), f'{scriptcommand}'):
        del simauto_obj
    scriptcommand = 'SolvePowerFlow(RECTNEWT)'
    if not CheckResultForError(simauto_obj.RunScriptCommand(scriptcommand), f'{scriptcommand}'):
        del simauto_obj
    SimAutoOutput = simauto_obj.GetParametersMultipleElement('LOAD', loadparamlist, '')
    if not CheckResultForError(SimAutoOutput, 'GetParameters'):
        del simauto_obj
    print(f'type of Output: {type(SimAutoOutput)}, {SimAutoOutput}')
    # print(f'{type(SimAutoOutput[1][1])},{SimAutoOutput[1][1]}')
 
 
## HELICSAUTO: Destroy
grantedtime = h.helicsFederateRequestTime(fed, h.HELICS_TIME_MAXTIME)
status = h.helicsFederateDisconnect(fed)
h.helicsFederateFree(fed)
h.helicsCloseLibrary()
 
del simauto_obj
