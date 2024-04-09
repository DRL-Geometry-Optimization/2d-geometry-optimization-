import numpy as np

def reward(efficiency, efficiency_param=1, cl_reward = False, cl = None, cl_target = None, cl_maxreward = 40, cl_wide = 15, delta_reward = False, last_efficiency = None):
    # Delta Reward True
    if delta_reward == True:
        print("Warning: Delta Reward is activated. This function is still under development")
        # Cl target False
        if cl_target == False:
            try:
                return efficiency - last_efficiency
            except:
                raise TypeError("Reward could not be calculated. The value of Last Efficiency was not introduced and Delta Reward is activated")
        # Cl target True
        else:
            print("Warning: cl_target or cd_target = True was not defined yet as a reward function. Returning delta efficiency as reward")
            return efficiency - last_efficiency
        

    # Delta Reward False
    else:
        # Cl target False
        if cl_reward == False:
            return efficiency_param*efficiency
        # Cl target True
        else:
            delta_Cl = cl - cl_target
            return efficiency_param*efficiency + cl_maxreward*np.exp(-cl_wide*(delta_Cl)**2)
    


    
