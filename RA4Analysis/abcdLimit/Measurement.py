from math import sqrt

class Measurement:
    """Class holding a value and its uncertainty.
    """

    def __init__(self,value=0.,error=None,errorSquared=None):
        """Initialize with value and uncertainty and/or uncertainty-squared.
        No check for consistency is performed!
        """
        self.value_ = value
        self.error_ = error
        if errorSquared!=None:
            self.eSquare_ = errorSquared
        else:
            if error!=None:
                self.eSquare_ = error**2
            else:
                self.eSquare_ = None

    def value(self):
        """Return the value.
        """
        return self.value_

    def error(self):
        """Return the uncertainty.
        """
        if self.error_==None:
            self.error_ = sqrt(self.eSquare_)
        return self.error_

    def errorSquared(self):
        """Return the square of the uncertainty.
        """
        if self.eSquare_==None:
            self.eSquare_ = self.error_**2
        return self.eSquare_

    def setError(self,error):
        """Set uncertainty & invalidate uncertainty**2
        """
        self.error_ = error
        self.eSquare_ = None

    def setErrorSquared(self,eSquare):
        """Set uncertainty**2 & invalidate uncertainty
        """
        self.eSquare_ = eSquare
        self.error_ = None

    def copy(self,other):
        """Copy data fom another instance.
        """
        self.value_ = other.value_
        self.error_ = other.error_
        self.eSquare_ = other.eSquare_

    def __add__(self,other):
        return Measurement(self.value_+other.value_,error=None, \
                           errorSquared=self.errorSquared()+other.errorSquared())

    def __sub__(self,other):
        return Measurement(self.value_-other.value_,error=None, \
                           errorSquared=self.errorSquared()+other.errorSquared())

    def __mul__(self,other):
        e2 = other.value_**2*self.errorSquared() + self.value_**2*other.errorSquared()
        return Measurement(self.value_*other.value_,error=None,errorSquared=e2)

    def __div__(self,other):
        if other.value_==0:
            return Measurement(float('Inf'),float('Inf'),float('Inf'))
        v = self.value_ / other.value_
        e2 = (self.errorSquared() + v**2*other.errorSquared()) / other.value_**2
        return Measurement(v,error=None,errorSquared=e2)

    def __iadd__(self,other):
        if type(other)==type(self):
            self.value_ += other.value_
            self.error_ = None
            self.setErrorSquared(self.errorSquared() + other.errorSquared())
        else:
            self.value_ += other
        return self

    def __isub__(self,other):
        if type(other)==type(self):
            self.value_ -= other.value_
            self.error_ = None
            self.eSquare_ = self.errorSquared() + other.errorSquared()
        else:
            self.value_ -= other
        return self

    def __imul__(self,other):
        if type(other)==type(self):
            self.copy(self*other)
        else:
            self.value_ *= other
            self.error_ *= other
            self.eSquare_ = None
        return self

    def __idiv__(self,other):
        if type(other)==type(self):
            if other.value_==0:
                self.value_ = float('Inf')
                self.error_ = float('Inf')
                self.eSquare_ = float('Inf')
            else:
                self.copy(self/other)
        else:
            if other.value_==0:
                self.value_ = float('Inf')
                self.error_ = float('Inf')
                self.eSquare_ = float('Inf')
            else:
                self.value_ /= other
                self.error_ /= other
                self.eSquare_ = None
        return self

    def __str__(self):
        return str(self.value_) + " +- " + str(self.error())
