import pandapower as pp
import pandapower.networks as pn
import numpy as np
# import random
 
net = pn.case33bw()
#print(net)
#print(net.ext_grid)
#print(net.load)
#print(net.sgen)
#print(net.load.loc[0, 'bus'])
pp.runpp(net)
print(net.res_ext_grid)
#print(net.res_bus.vm_pu)
original_load = net.load.loc[:, 'p_mw'].to_numpy()
print(f'original load is {original_load}')
print(f'original load is: {type(original_load)} {original_load.size}')
n_load = original_load.size
np.random.seed(1)
 
 
 
## HELICSAUTO: Register
import helics as h
fed = h.helicsCreateValueFederateFromConfig('../pandapower/fed_config.json')
 
## HELICSAUTO: Execute
h.helicsFederateEnterExecutingMode(fed)
hours = 1
total_interval = int(60 * 60 * hours)
update_interval = int(h.helicsFederateGetTimeProperty(fed, h.HELICS_PROPERTY_TIME_PERIOD))
grantedtime = 0
while grantedtime < total_interval:
 
    # change load to see the pf results
    load_var = np.random.randint(low = 90, high = 110, size = n_load) / 100
    #print(f'load_var is {load_var}')
    # net.load.loc[:, 'p_mw'] = net.load.loc[:, 'p_mw'] * 1.1
    new_load = np.multiply(original_load, load_var)
    print(f'new load is : {new_load}')
    net.load.loc[:, 'p_mw'] = new_load
    pp.runpp(net)
    print(net.res_ext_grid)
    print(type(net.res_ext_grid.loc[0, 'p_mw']))
    feeder_p_mw = net.res_ext_grid.loc[0, 'p_mw']
    feeder_q_mvar = net.res_ext_grid.loc[0, 'q_mvar']
    feeder_s = complex(feeder_p_mw, feeder_q_mvar)
    print(f'feeder_s: {feeder_s.real} + j {feeder_s.imag}')
    ## HELICSAUTO: Publish, feeder_s, complex, TransmissionSim/transmission_volta
    pubid = h.helicsFederateGetPublication(fed, 'TransmissionSim/transmission_volta')
    status = h.helicsPublicationPublishComplex(pubid, feeder_s.real, feeder_s.imag)
 
## HELICSAUTO: Destroy
grantedtime = h.helicsFederateRequestTime(fed, h.HELICS_TIME_MAXTIME)
status = h.helicsFederateDisconnect(fed)
h.helicsFederateFree(fed)
h.helicsCloseLibrary()
