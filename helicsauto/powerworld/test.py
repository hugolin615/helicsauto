#!/usr/bin/env python
# coding: utf-8
 
 
import numpy as np
 
 
 
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
 
     
    ## HELICSAUTO: Sync
    requested_time = grantedtime + update_interval
    grantedtime = h.helicsFederateRequestTime(fed, requested_time)
 
    feeder_var = complex(0, 0)
    ## HELICSAUTO: Subscribe, feeder_var, complex, Feeder_S 
    subid = h.helicsFederateGetSubscription(fed, 'Feeder_S')
    feeder_var = h.helicsInputGetComplex((subid))
    print(f'subscription: {feeder_var}')
 
     
## HELICSAUTO: Destroy
grantedtime = h.helicsFederateRequestTime(fed, h.HELICS_TIME_MAXTIME)
status = h.helicsFederateDisconnect(fed)
h.helicsFederateFree(fed)
h.helicsCloseLibrary()
 
