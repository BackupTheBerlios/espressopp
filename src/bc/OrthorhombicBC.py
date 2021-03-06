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
************************************
**OrthorhombicBC** - Object
************************************

Like all boundary condition objects, this class implements
all the methods of the base class **BC** , which are described in detail
in the documentation of the abstract class **BC**.

The OrthorhombicBC class is responsible for the orthorhombic boundary condition.
Currently only periodic boundary conditions are supported.

Example: 

>>> boxsize = (Lx, Ly, Lz)
>>> bc = espresso.bc.OrthorhombicBC(rng, boxsize) 

"""

from espresso.esutil import cxxinit
from espresso import pmi
from espresso import toReal3D

from espresso.bc.BC import *
from _espresso import bc_OrthorhombicBC 

class OrthorhombicBCLocal(BCLocal, bc_OrthorhombicBC):
    def __init__(self, rng, boxL=1.0):
        if not (pmi._PMIComm and pmi._PMIComm.isActive()) or pmi._MPIcomm.rank in pmi._PMIComm.getMPIcpugroup() or pmi.isController:
            cxxinit(self, bc_OrthorhombicBC, rng, toReal3D(boxL))

    # override length property
    def setBoxL(self, boxL):
        if not (pmi._PMIComm and pmi._PMIComm.isActive()) or pmi._MPIcomm.rank in pmi._PMIComm.getMPIcpugroup():
            self.cxxclass.boxL.fset(self, toReal3D(boxL))

    boxL = property(bc_OrthorhombicBC.boxL.fget, setBoxL)

if pmi.isController :
    class OrthorhombicBC(BC):
        pmiproxydefs = dict(
            cls =  'espresso.bc.OrthorhombicBCLocal',
            pmiproperty = [ 'boxL' ]
            )
