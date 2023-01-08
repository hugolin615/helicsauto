import time
import random
#import logging
import numpy as np
 
if __name__ == "__main__":
 
    # based on fundamental_default/Battery.py
 
    np.random.seed(628)
 
    ##########  Registering  federate and configuring from JSON################
    ## HELICSAUTO: Register
    import helics as h
    fed = h.helicsCreateValueFederateFromConfig('../help/fed_config.json')
 
    ## HELICSAUTO: Execute
    h.helicsFederateEnterExecutingMode(fed)
    hours = 1
    total_interval = int(60 * 60 * hours)
    update_interval = int(h.helicsFederateGetTimeProperty(fed, h.HELICS_PROPERTY_TIME_PERIOD))
    grantedtime = 0
    while grantedtime < total_interval:
 
        c = complex(132790.562, 0) * (1 + (random.random() - 0.5)/2)
        ## HELICSAUTO: Publish, c, complex, TransmissionSim/transmission_voltage
        pubid = h.helicsFederateGetPublication(fed, 'TransmissionSim/transmission_voltage')
        status = h.helicsPublicationPublishComplex(pubid, c.real, c.imag)
 
        ## HELICSAUTO: Sync
        requested_time = grantedtime + update_interval
        grantedtime = h.helicsFederateRequestTime(fed, requested_time)
 
        #rValue, iValue = h.helicsInputGetComplex((subid))
        # temp = h.helicsInputGetComplex((subid))
        temp = 0.0
        ## HELICSAUTO: Subscribe, temp, complex, IEEE_123_feeder_0/totalLoad
        subid = h.helicsFederateGetSubscription(fed, 'IEEE_123_feeder_0/totalLoad')
        temp = h.helicsInputGetComplex((subid))
        print(f'DEBUG: what is intpu get: {temp} ')
        #logger.info("Python Federate grantedtime = {}".format(grantedtime))
        #logger.info("Load value = {} MVA".format(complex(rValue, iValue)/1000))
 
 
    ## HELICSAUTO: Destroy
    grantedtime = h.helicsFederateRequestTime(fed, h.HELICS_TIME_MAXTIME)
    status = h.helicsFederateDisconnect(fed)
    h.helicsFederateFree(fed)
    h.helicsCloseLibrary()
