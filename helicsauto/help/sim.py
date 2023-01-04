import time
import random
#import logging
import numpy as np

if __name__ == "__main__":
    
    # based on fundamental_default/Battery.py

    np.random.seed(628)

    ##########  Registering  federate and configuring from JSON################
    ## HELICSAUTO: Register
    
    ## HELICSAUTO: Execute
    
    c = complex(132790.562, 0) * (1 + (random.random() - 0.5)/2)
    ## HELICSAUTO: Publish, c, complex, TransmissionSim/transmission_voltage

    #rValue, iValue = h.helicsInputGetComplex((subid))
    # temp = h.helicsInputGetComplex((subid))
    temp = 0.0
    ## HELICSAUTO: Subscribe, temp, complex, IEEE_123_feeder_0/totalLoad
    print(f'DEBUG: what is intpu get: {temp} ')
    #logger.info("Python Federate grantedtime = {}".format(grantedtime))
    #logger.info("Load value = {} MVA".format(complex(rValue, iValue)/1000))


    ## HELICSAUTO: Destroy
