#ifndef BinContentTriplet_h_
#define BinContentTriplet_h_
struct BinContentTriplet {
  BinContentTriplet () : x_(0), y_(0), z_(0.) {}
  BinContentTriplet (int x, int y, double z) : x_(x), y_(y), z_(z) {}
  inline int x () const {return x_;}
  inline int y () const {return y_;}
  inline double z () const {return z_;}
  int x_,y_;
  double z_;
};
#endif

