// ESPP_CLASS
#ifndef _TRIPLE_HPP
#define _TRIPLE_HPP

#include "types.hpp"

namespace espresso {

  template <class T1, class T2, class T3> struct Triple {

    typedef T1 first_type;
    typedef T2 second_type;
    typedef T3 third_type;

    T1 first;
    T2 second;
    T3 third;

    Triple() : first(T1()),
	       second(T2()),
	       third(T3())
	       { }

    Triple(const T1& x, const T2& y, const T3& z) : first(x),
						    second(y),
						    third(z)
						    { }

    template <class U, class V, class W>
    Triple (const Triple<U, V, W> &p) : first(p.first),
					second(p.second),
					third(p.third)
					{ }

    inline bool operator== (const Triple &T) const {
      return (first == T.first) && (second == T.second) && (third == T.third);
    }

  };

}
#endif
