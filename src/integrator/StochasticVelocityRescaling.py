#  Copyright (C) 2012,2013
#      Max Planck Institute for Polymer Research
#  Copyright (C) 2008,2009,2010,2011
#      Max-Planck-Institute for Polymer Research & Fraunhofer SCAI
#  
#  This file is part of ESPResSo++.
#  
#  ESPResSo++ is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  ESPResSo++ is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>. 


"""
***************************************************
**espresso.integrator.StochasticVelocityRescaling**
***************************************************

"""
from espresso.esutil import cxxinit
from espresso import pmi

from espresso.integrator.Extension import *
from _espresso import integrator_StochasticVelocityRescaling 

class StochasticVelocityRescalingLocal(ExtensionLocal, integrator_StochasticVelocityRescaling):
    'The (local) StochasticVelocityRescaling Thermostat.'
    def __init__(self, system):
        if not (pmi._PMIComm and pmi._PMIComm.isActive()) or pmi._MPIcomm.rank in pmi._PMIComm.getMPIcpugroup():
            cxxinit(self, integrator_StochasticVelocityRescaling, system)

if pmi.isController :
    class StochasticVelocityRescaling(Extension):
        __metaclass__ = pmi.Proxy
        pmiproxydefs = dict(
            cls =  'espresso.integrator.StochasticVelocityRescalingLocal',
            pmiproperty = [ 'temperature', 'coupling' ]
        )
