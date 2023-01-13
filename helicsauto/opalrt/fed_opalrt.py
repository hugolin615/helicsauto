import sys
sys.path.append(r'C:\OPAL-RT\HYPERSIM\hypersim_2021.1.1.o137\Windows\HyApi\C\py')
 
import HyWorksApi
import time
HyWorksApi.startAndConnectHypersim()
designPath = r'C:\OPAL-RT\HYPERSIM\hypersim_2021.1.1.o137\Windows\demo\Transmission\HVAC_735KV_38BUS.ecf'
HyWorksApi.openDesign(designPath)
 
HyWorksApi.setPreference('simulation.calculationStep', '50e-6')
calcStep = HyWorksApi.getPreference('simulation.calculationStep')
 
print('calcStep = ' + calcStep)
print('code directory : ' + HyWorksApi.getPreference('simulation.codeDirectory'))
print('mode : ' + HyWorksApi.getPreference('simulation.architecture'))
 
HyWorksApi.mapTask()
HyWorksApi.genCode()
HyWorksApi.startLoadFlow()
HyWorksApi.startSim()
 
time.sleep(10)
print('startSim done')
 
## HELICSAUTO: Register
import helics as h
fed = h.helicsCreateValueFederateFromConfig('../opalrt/opalrt_config.json')
 
## HELICSAUTO: Execute
h.helicsFederateEnterExecutingMode(fed)
hours = 1
total_interval = int(60 * 60 * hours)
update_interval = int(h.helicsFederateGetTimeProperty(fed, h.HELICS_PROPERTY_TIME_PERIOD))
grantedtime = 0
while grantedtime < total_interval:
 
 
    ## HELICSAUTO: Sync
    requested_time = grantedtime + update_interval
    grantedtime = h.helicsFederateRequestTime(fed, requested_time)
 
    feeder_var = complex(0, 0)
    ## HELICSAUTO: Subscribe, feeder_var, complex, Feeder_S
    subid = h.helicsFederateGetSubscription(fed, 'Feeder_S')
    feeder_var = h.helicsInputGetComplex((subid))
 
    # change load at Ld18
 
    get_load = HyWorksApi.getComponentParameter('Ld18','pBase')
    print('Before changing load at Ld18 = ' + get_load[0] + get_load[1])
    #new_load = str(int(get_load[0]) + 11000000)
    new_load = str(int(get_load[0]) + int(feeder_var.real * 1000))
    HyWorksApi.setComponentParameter('Ld18','pBase', new_load)
    get_load_change = HyWorksApi.getComponentParameter('Ld18','pBase')
    print('After changing load at Ld18 = ' + get_load_change[0] + get_load_change[1] )
 
## HELICSAUTO: Destroy
grantedtime = h.helicsFederateRequestTime(fed, h.HELICS_TIME_MAXTIME)
status = h.helicsFederateDisconnect(fed)
h.helicsFederateFree(fed)
h.helicsCloseLibrary()
 
time.sleep(10)
HyWorksApi.stopSim()
HyWorksApi.closeDesign(designPath)
HyWorksApi.closeHyperWorks()
