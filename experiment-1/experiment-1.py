import sys
sys.path.append("..")

import tools.spice as spice
import tools.latex as latex

spice.set_filename("experiment-1")
latex.set_filename("experiment-1")

variables = {}
spice.get_variables(variables)
latex.generate_variables(variables)