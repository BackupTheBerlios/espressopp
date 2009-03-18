#ifndef _PAIRS_COMPUTER_HPP
#define _PAIRS_COMPUTER_HPP

#include "types.hpp"
#include "particles/Set.hpp"

namespace espresso {
  namespace pairs {
    /** Abstract class that defines the operator() applied to particle pairs
     */
    template<class ParticleReference>
    class ComputerBase {
      
    public:
      /// @name extended function object interface
      //@{
      typedef esutil::Real3D first_argument_type;
      typedef ParticleReference second_argument_type;
      typedef ParticleReference  third_argument_type;
      typedef void                       result_type;
      //@}

      /** Interface of the routine that is applied to particle pairs
	  \param dist: distance vector between the two particles
	  \param p1, p2: references to the two particles

	  Note: The references are necessary if more property data of the particles is
	  needed than only the distance.
      */
      virtual void operator()(const esutil::Real3D &dist, 
			      const ParticleReference p1, 
			      const ParticleReference p2) = 0;
    };

    /** Abstract class that defines a function on pairs of particles */
    class Computer: 
      public ComputerBase<particles::ParticleReference> 
    {};
    
    /** Abstract class that defines a function on pairs of read-only particles */
    class ConstComputer:
      public ComputerBase<particles::ConstParticleReference> 
    {};
  }
}

#endif