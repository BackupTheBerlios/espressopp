#ifndef _BC_HPP
#define _BC_HPP

#include "types.hpp"

namespace espresso {
  class Real3D;
  class Real3DRef;

    /** Abstract base class for boundary conditions. */
  class BC {
  public:
    /** Virtual destructor for boundary conditions. */
    virtual ~BC() {};

    /** Method to set the length of the side of the simulation box */
    virtual void
    setBoxL(const ConstReal3DRef _boxL) = 0;
      
    /** Getters for box dimensions */
    virtual Real3D getBoxL() = 0;
    virtual real getBoxL(int i)      const = 0;

    virtual Real3D getInvBoxL() = 0;
    virtual real getInvBoxL(int i)   const = 0;

    /** Computes the minimum image distance vector between two
	positions. This routine must be implemented by derived
	classes (once the code stabilizes).

	\param dist is the distance vector (pos2 - pos1)
	\param distSqr is the square of the magnitude
	of the separation vector
	\param pos1, pos2 are the particle positions 
    */
    virtual void
    getMinimumImageVector(Real3DRef dist,
			  real &distSqr,
			  const ConstReal3DRef pos1,
			  const ConstReal3DRef pos2) const = 0;

    /** fold a coordinate to the primary simulation box.
	\param pos         the position...
	\param imageBox    and the box
	\param dir         the coordinate to fold: dir = 0,1,2 for x, y and z coordinate.

	Both pos and image_box are I/O,
	i. e. a previously folded position will be folded correctly.
    */
    virtual void foldCoordinate(Real3DRef pos, int imageBox[3], int dir) = 0;

    /** fold particle coordinates to the primary simulation box.
	\param pos the position...
	\param imageBox and the box

	Both pos and image_box are I/O,
	i. e. a previously folded position will be folded correctly.
    */
    virtual void foldPosition(Real3DRef pos, int imageBox[3]) = 0;

    /** unfold coordinates to physical position.
	\param pos the position...
	\param imageBox and the box
	
	Both pos and image_box are I/O, i.e. image_box will be (0,0,0)
	afterwards.
    */
    virtual void unfoldPosition(Real3DRef pos, int imageBox[3]) = 0;

    /** Get a random position within the central simulation box. The
	positions are assigned with each coordinate on [0, boxL]. */
    virtual void
    getRandomPos(Real3DRef res) const = 0;

    virtual Real3D
    getRandomPos() const;

    static void registerPython();

  }; 
}

#endif