import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p
import neuralfoil as nf
import time
import random




class airfoiltools:
    """
    This class provides tools for working with one airfoil.

    Attributes:
        airfoil: A placeholder for the airfoil object.
        aerodynamics: A placeholder for the aerodynamics of the airfoil.
        upparameters: A placeholder for the parameters of the upper side of the airfoil.
        downparameters: A placeholder for the parameters of the lower side of the airfoil.
    """

    def __init__(self):
        self.airfoil = None # Placeholder for the airfoil object
        self.aerodynamics = None # Placeholder for the aerodynamics of the airfoil 
        self.upparameters = None # Placeholder for the number of parameters of the airfoil
        self.downparameters = None



    def kulfan(self, lower_weights, upper_weights, leading_edge_weight, TE_thickness = 0, name = ""):
        self.upparameters = len(upper_weights) # Number of parameters in the upper side of the airfoil
        self.downparameters = len(lower_weights)
        self.airfoil = asb.KulfanAirfoil( # Create the airfoil object with the Kulfan parameterization
        name=name,
        lower_weights=lower_weights,
        upper_weights=upper_weights,
        leading_edge_weight=leading_edge_weight,
        TE_thickness=TE_thickness
        )

    # Randomize the weights of the airfoil
    def random_kulfan(self, n_params = 15, variation = 0.1, thickness = 1.1):
        
        np.random.seed(int(time.time())) # Seed the random number generator with the current time

        leading_edge_weight = random.uniform(-variation*3, variation*3) # Randomize the leading edge weight
        TE_thickness = 0 # Thickness of the trailing edge
        
        lower_weights = np.zeros(n_params) # Initialize the lower weights
        
        for i in range(len(lower_weights)): # Randomize the lower weights
            if i == 0: # Skip the first weight
                lower_weights[i] = random.uniform(-leading_edge_weight-variation, -leading_edge_weight+variation) # Randomize the first weight
            else:
                lower_weights[i] = random.uniform(lower_weights[i-1] - variation, lower_weights[i-1] + variation)

        upper_weights = np.zeros(n_params) # Initialize the upper weights
        for i in range(len(lower_weights)): # Randomize the upper weights based on the lower weights (to not have intersections)
            if i == 0:
                upper_weights[i] = random.uniform(lower_weights[i], lower_weights[i]+variation)
            else:
                upper_weights[i] = random.uniform(lower_weights[i], upper_weights[i-1] + variation)

        lower_weights = lower_weights * thickness # Scale the lower weights
        upper_weights = upper_weights * thickness

        # Create the airfoil
        self.kulfan(lower_weights, upper_weights, leading_edge_weight, TE_thickness)



    # Randomize the airfoil with a different method. This methods parts from the upper and lower weights and randomizes them separately
    # Randomize the weights of the airfoil   
    def random_kulfan2(self, n_params = 15, variation = 0.5, extra_weight = 0.5, intra_weight = 0.2): 
        np.random.seed(int(time.time()))

        leading_edge_weight = random.uniform(-variation*3, variation*3) # Randomize the leading edge weight
        TE_thickness = 0 # Thickness of the trailing edge

        lower_weights = np.zeros(n_params) 

        for i in range(len(lower_weights)):
            lower_weights[i] = random.uniform(-intra_weight-variation, -intra_weight+variation) # Randomize the first weight
        
        upper_weights = np.zeros(n_params) 
        for i in range(len(lower_weights)): 
            if extra_weight-variation < lower_weights[i]: # if lower weight can be higher than the extra weight
                upper_weights[i] = random.uniform(lower_weights[i], extra_weight+variation)
            else:
                upper_weights[i] = random.uniform(extra_weight-variation, extra_weight+variation)


        # Create the airfoil
        self.kulfan(lower_weights, upper_weights, leading_edge_weight, TE_thickness)


    # Modify the airfoil by changing the weights of the parameters.
    # The weights are added to the existing weights of the airfoil!
    def modify_airfoil(self, action, TE_thickness = 0, name = ""):
        self.airfoil.upper_weights = self.airfoil.upper_weights + action[1]
        self.airfoil.lower_weights = self.airfoil.lower_weights + action[0]
        self.airfoil.leading_edge_weight = self.airfoil.leading_edge_weight + action[2]
        self.airfoil.TE_thickness = self.airfoil.TE_thickness + TE_thickness
        self.airfoil.name = name # Change the name of the airfoil if needed



    # Modify the airfoil by changing the weight of a parameter
    def modify_airfoil_unit(self, face, index, variation):  
        try:
            if face == "up":
                self.airfoil.upper_weights[index] = self.airfoil.upper_weights[index] + variation
            elif face == "down":
                self.airfoil.lower_weights[index] = self.airfoil.lower_weights[index] + variation
            else:
                raise ValueError("Invalid face. Please, use 'up' or 'down'") # Raise an error if the face is not up or down
        except IndexError: # except the index error if the index is out of bounds
            print(f"Index out of bounds. Probably the airfoil has less weights than {index}")
        except Exception as e: # except any other error
            print(f"Error: {e}")
            


    def analysis(self, angle = 0, re = 1e6, model = "xlarge"): # Analyze the airfoil and save into the aerodynamics attribute (dictionary)
        self.aerodynamics = nf.get_aero_from_kulfan_parameters(
            self.airfoil.kulfan_parameters, 
            angle, re, 
            model)



    def get_cl(self):  
        if self.aerodynamics is None:
            # Raise an error shoud be changed if you do not want to stop the program. The other option is to return None
            raise ValueError("Please, analyze the airfoil first") 
        return self.aerodynamics["CL"][0]
        


    def get_cd(self):  
        if self.aerodynamics is None:
            raise ValueError("Please, analyze the airfoil first")
        return self.aerodynamics["CD"][0]



    def get_efficiency(self):
        try:
            cl = self.get_cl()
            cd = self.get_cd()
            return cl/cd
        except ValueError as e:
            raise ValueError(f"An unexpected error occurred while obtaining efficiency: {e}")
        


    def airfoil_plot(self): # Plot the airfoil 
        fig, ax = plt.subplots(figsize=(6, 2))
        self.airfoil.draw()






if __name__ == "__main__": #This will only run if the script is run directly, not imported
    # Test the airfoiltools class
    pedro = airfoiltools()
    pedro.random_kulfan2(15, 0., 0.3, 0.1)
    pedro.analysis()
    pedro.airfoil_plot()
    #print(pedro.get_cl())
    #print(pedro.get_cd())
    #print(pedro.get_efficiency())

    print(pedro.airfoil.upper_weights)
    print(pedro.airfoil.lower_weights)

    pedro.modify_airfoil(np.full(15, 0.3), np.full(15, -0.1), 0.1)
    
    pedro.analysis()
    pedro.airfoil_plot()

    print(pedro.airfoil.upper_weights)
    print(pedro.airfoil.lower_weights)
    #print(pedro.get_cl())
    #print(pedro.get_cd())
    #print(pedro.get_efficiency())