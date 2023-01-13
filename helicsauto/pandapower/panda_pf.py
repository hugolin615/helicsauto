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

## HELICSAUTO: Execute

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
## HELICSAUTO: Publish, feeder_s, complex, Feeder_S

## HELICSAUTO: Sync

## HELICSAUTO: Destroy
