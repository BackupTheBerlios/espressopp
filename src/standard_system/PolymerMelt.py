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
****************************************
**espresso.standard_system.PolymerMelt**
****************************************

"""
import espresso
import mpi4py.MPI as MPI
import sys

def PolymerMelt(num_chains, monomers_per_chain, box=(0,0,0), bondlen=0.97, rc=1.12246, skin=0.3, dt=0.005, epsilon=1.0, sigma=1.0, shift='auto', temperature=None, xyzfilename=None, xyzrfilename=None):
  '''
  returns random walk polymer melt system and integrator:
  if tempearture is != None then Langevin thermostat is set to temperature (gamma is 1.0)
  '''

  if xyzfilename and xyzrfilename:
     print "ERROR: only one of xyzfilename (only xyz data) or xyzrfilename (additional particle radius data) can be provided."
     sys.exit(1)

  if xyzrfilename: 
    pidf, typef, xposf, yposf, zposf, xvelf, yvelf, zvelf, Lxf, Lyf, Lzf, radiusf = espresso.tools.readxyzr(xyzrfilename)
    box = (Lxf, Lyf, Lzf)
  elif xyzfilename:
    pidf, typef, xposf, yposf, zposf, xvelf, yvelf, zvelf, Lxf, Lyf, Lzf = espresso.tools.readxyz(xyzfilename)
    box = (Lxf, Lyf, Lzf)
  else:
    if box[0]<=0 or box[1]<=0 or box[2]<=0:
      print "WARNING: no valid box size specified, box size set to (100,100,100) !"

  system         = espresso.System()
  system.rng     = espresso.esutil.RNG()
  system.bc      = espresso.bc.OrthorhombicBC(system.rng, box)
  system.skin    = skin
  nodeGrid       = espresso.tools.decomp.nodeGrid(MPI.COMM_WORLD.size)
  cellGrid       = espresso.tools.decomp.cellGrid(box, nodeGrid, rc, skin)
  system.storage = espresso.storage.DomainDecomposition(system, nodeGrid, cellGrid)
  interaction    = espresso.interaction.VerletListLennardJones(espresso.VerletList(system, cutoff=rc))
  interaction.setPotential(type1=0, type2=0, potential=espresso.interaction.LennardJones(epsilon, sigma, rc, shift))
  system.addInteraction(interaction)
  
  integrator     = espresso.integrator.VelocityVerlet(system)  
  integrator.dt  = dt
  if (temperature != None):
    thermostat             = espresso.integrator.LangevinThermostat(system)
    thermostat.gamma       = 1.0
    thermostat.temperature = temperature
    integrator.addExtension(thermostat)

  mass     = 1.0  

  if xyzrfilename: 
    props    = ['id', 'type', 'mass', 'pos', 'v', 'radius']
    bondlist = espresso.FixedPairList(system.storage)
    for i in range(num_chains):
      chain = []
      bonds = []
      for k in range(monomers_per_chain):
        idx  =  i * monomers_per_chain + k
        part = [ pidf[idx], typef[idx], mass,
                 espresso.Real3D(xposf[idx],yposf[idx],zposf[idx]),
                 espresso.Real3D(xvelf[idx],yvelf[idx],zvelf[idx]),
                 radiusf[idx] ]
        chain.append(part)
        if k>0:
          bonds.append((pidf[idx-1], pidf[idx]))
      system.storage.addParticles(chain, *props)
      system.storage.decompose()
      bondlist.addBonds(bonds)
  elif xyzfilename: 
    props    = ['id', 'type', 'mass', 'pos', 'v']
    bondlist = espresso.FixedPairList(system.storage)
    for i in range(num_chains):
      chain = []
      bonds = []
      for k in range(monomers_per_chain):
        idx  =  i * monomers_per_chain + k
        part = [ pidf[idx], typef[idx], mass,
                 espresso.Real3D(xposf[idx],yposf[idx],zposf[idx]),
                 espresso.Real3D(xvelf[idx],yvelf[idx],zvelf[idx])]
        chain.append(part)
        if k>0:
          bonds.append((pidf[idx-1], pidf[idx]))
      system.storage.addParticles(chain, *props)
      system.storage.decompose()
      bondlist.addBonds(bonds)
  else:            
    props    = ['id', 'type', 'mass', 'pos', 'v']
    vel_zero = espresso.Real3D(0.0, 0.0, 0.0)
    bondlist = espresso.FixedPairList(system.storage)
    pid      = 1
    type     = 0
    chain    = []
    for i in range(num_chains):
      startpos = system.bc.getRandomPos()
      positions, bonds = espresso.tools.topology.polymerRW(pid, startpos, monomers_per_chain, bondlen)
      for k in range(monomers_per_chain):  
        part = [pid + k, type, mass, positions[k], vel_zero]
        chain.append(part)
      pid += monomers_per_chain
      type += 1
      system.storage.addParticles(chain, *props)
      system.storage.decompose()
      chain = []
      bondlist.addBonds(bonds)

  system.storage.decompose()

  # FENE bonds
  potFENE   = espresso.interaction.FENE(K=30.0, r0=0.0, rMax=1.5)
  interFENE = espresso.interaction.FixedPairListFENE(system, bondlist, potFENE)
  system.addInteraction(interFENE)
    
  return system, integrator
  
  
  class KGMelt:
    def __init__(self, num_chains, chain_len):
      self._num_chains    = num_chains
      self._chain_len     = chain_len
      self._num_particles = num_chains * chain_len
      self._density       = 0.8449
      self._L             = pow(self._num_particles / self._density, 1.0/3.0)
      self._box           = (L, L, L)
      self._system        = espress.System()

