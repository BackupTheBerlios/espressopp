#include "python.hpp"
#include <cmath>
#include "Pressure.hpp"
#include "storage/DomainDecomposition.hpp"
#include "iterator/CellListIterator.hpp"
#include "bc/BC.hpp"
#include "interaction/Interaction.hpp"
#include "interaction/Potential.hpp"
#include "VerletList.hpp"

using namespace espresso;
using namespace iterator;
using namespace interaction;

namespace espresso {
  namespace analysis {
    real Pressure::compute() const {

      System& system = getSystemRef();
  
      // determine volume of the box
      Real3D Li = system.bc->getBoxL();
      real tripleV = 3.0 * Li[0] * Li[1] * Li[2];

      // compute the kinetic contriubtion (2/3 \sum 1/2mv^2)
      real p_kinetic;
      real v2sum;
      real v2 = 0.0;

      CellList realCells = system.storage->getRealCells();
      for (CellListIterator cit(realCells); !cit.isDone(); ++cit) {
        const Particle& p = *cit;
        v2 = v2 + p.mass() * (p.velocity() * p.velocity());
      }
      boost::mpi::all_reduce(*mpiWorld, v2, v2sum, std::plus<real>());
      p_kinetic = v2sum / tripleV;
      
      // compute the short-range nonbonded contribution
      real rij_dot_Fij = 0.0;

      const InteractionList& srIL = system.shortRangeInteractions;
      for (size_t j = 0; j < srIL.size(); j++) {
        rij_dot_Fij += srIL[j]->computeVirial();
      }

      real p_nonbonded = rij_dot_Fij / tripleV;
      // computeVirial() returns already reduced value
      //mpi::all_reduce(*mpiWorld, rij_dot_Fij / (3.0 * V), p_nonbonded, std::plus<real>());
 
      return (p_kinetic + p_nonbonded);
    }

    void Pressure::registerPython() {
      using namespace espresso::python;
      class_<Pressure, bases< Observable > >
        ("analysis_Pressure", init< shared_ptr< System > >())
      ;
    }
  }
}
