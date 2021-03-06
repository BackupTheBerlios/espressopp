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
**espresso.FixedQuadrupleAngleList**
************************************

"""
from espresso import pmi
import _espresso
import espresso
from espresso.esutil import cxxinit

class FixedQuadrupleAngleListLocal(_espresso.FixedQuadrupleAngleList):
    'The (local) fixed quadruple list.'

    def __init__(self, storage):
        'Local construction of a fixed quadruple list'
        if pmi.workerIsActive():
            cxxinit(self, _espresso.FixedQuadrupleAngleList, storage)

    def add(self, pid1, pid2, pid3, pid4):
        'add quadruple to fixed quadruple list'
        if pmi.workerIsActive():
            return self.cxxclass.add(self, pid1, pid2, pid3, pid4)

    def size(self):
        'count number of Quadruples in GlobalQuadrupleList, involves global reduction'
        if pmi.workerIsActive():
            return self.cxxclass.size(self)

    def addQuadruples(self, quadruplelist):
        """
        Each processor takes the broadcasted quadruplelist and
        adds those quadruples whose first particle is owned by
        this processor.
        """

        if pmi.workerIsActive():
            for quadruple in quadruplelist:
                pid1, pid2, pid3, pid4 = quadruple
                self.cxxclass.add(self, pid1, pid2, pid3, pid4)

    def getQuadruples(self):
        'return the quadruples of the GlobalQuadrupleList'
        if pmi.workerIsActive():
          quadruple = self.cxxclass.getQuadruples(self)
          return quadruple 
        
    'returns the list of (pid1, pid2, pid3, pid4, angle(123))'
    def getQuadruplesAngles(self):
        'return the quadruples with angle'
        if pmi.workerIsActive():
          quadruples_angles = self.cxxclass.getQuadruplesAngles(self)
          return quadruples_angles
        
    def getAngle(self, pid1, pid2, pid3, pid4):
        if pmi.workerIsActive():
          return self.cxxclass.getAngle(self, pid1, pid2, pid3, pid4)

if pmi.isController:
  class FixedQuadrupleAngleList(object):
    __metaclass__ = pmi.Proxy
    pmiproxydefs = dict(
        cls = 'espresso.FixedQuadrupleAngleListLocal',
        localcall = [ "add" ],
        pmicall = [ "addQuadruples" ],
        pmiinvoke = ["getQuadruples", "getQuadruplesAngles", "size"]
    )
    
    def getAngle(self, pid1, pid2, pid3, pid4 ):
      angles = pmi.invoke(self.pmiobject, 'getAngle', pid1, pid2, pid3, pid4 )
      for i in angles:
        if( i != -1 ):
          return i        
