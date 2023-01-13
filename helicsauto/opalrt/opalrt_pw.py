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
    
## HELICSAUTO: Execute


## HELICSAUTO: Sync

feeder_var = complex(0, 0)
## HELICSAUTO: Subscribe, feeder_var, complex, Feeder_S

# change load at Ld18

get_load = HyWorksApi.getComponentParameter('Ld18','pBase')
print('Before changing load at Ld18 = ' + get_load[0] + get_load[1])
#new_load = str(int(get_load[0]) + 11000000)
new_load = str(int(get_load[0]) + int(feeder_var.real * 1000))
HyWorksApi.setComponentParameter('Ld18','pBase', new_load)
get_load_change = HyWorksApi.getComponentParameter('Ld18','pBase')
print('After changing load at Ld18 = ' + get_load_change[0] + get_load_change[1] )

## HELICSAUTO: Destroy

time.sleep(10)
HyWorksApi.stopSim()
HyWorksApi.closeDesign(designPath)
HyWorksApi.closeHyperWorks()
