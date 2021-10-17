def gcd(a, b):
    """Retrun greatest common devisor"""
    while b!= 0:
        c = a % b
        a = b
        b = c
    return a

def lcm(a, b):
    """Return least common multiple"""
    return a * (b // gcd(a ,b))

def float_2_frac(float_val):
    """Return numerator and denominator from float value"""
    den = 1
    while int(float_val) - float_val:
        den *= 10
        float_val *=10
    return int(float_val), den

class Fraction():
    """
    Fraction class

    Args
    ----
    p - numerator int or float
    q - denominator int [default = 1]
    
    if p is float then q argument is ommited and float is transformed to fraction
    """
    enhanced = False
    mixed = False

    @classmethod
    def change_version(cls):
        """Change to enhanced version or go back to standard version"""
        if cls.enhanced == True:
            cls.enhanced = False 
        else:
            cls.enhanced = True

    
    @classmethod
    def change_display(cls):
        """Change fraction representation to mixed or go back to standard representation"""
        if cls.mixed == True:
            cls.mixed = False
        else:
            cls.mixed = True

    def __init__(self, p, q = 1):
        p2, q2 = 1, 1

        if not type(q) is type(1):
            if Fraction.enhanced:
                if not type(q) is type(.1):
                    raise TypeError("Invalid denominator")
                q, p2 = float_2_frac(q)
            raise TypeError("Invalid denominator")

        if not q:
            raise ZeroDivisionError("Denominator musn' t be equal zero")
        

        if not type(p) is type(1):
            if Fraction.enhanced:
                if not type(p) is type(.1):
                    raise TypeError("Invalid numerator")
                p, q2 = float_2_frac(p)
            else:
                raise TypeError("Invalid numerator")
        
        p *= p2        
        q *= q2
        if q < 0: 
            p, q = p*(-1), q*(-1)
        reducer = gcd(p, q)
        self.__numerator = p // reducer
        self.__denominator = q // reducer
    
    def __str__(self):
        if not self.__numerator % self.__denominator:
            return str(self.__numerator / self.__denominator)
        if Fraction.mixed:
            total = abs(self.__numerator) // self.__denominator
            other = abs(self.__numerator) % self.__denominator
            if total:
                if self.__numerator >= 0 :
                    return "{} + {}/{}".format(total,other,self.__denominator)
                return "-{} - {}/{}".format(total,other,self.__denominator)
                    
        return "{}/{}".format(self.__numerator, self.__denominator)
    
    def __repr__(self):
        if not self.__numerator % self.__denominator:
            return str(self.__numerator / self.__denominator)
        if Fraction.mixed:
            total = abs(self.__numerator) // self.__denominator
            other = abs(self.__numerator) % self.__denominator
            if total:
                if self.__numerator >= 0 :
                    return "{} + {}/{}".format(total,other,self.__denominator)
                return "-{} - {}/{}".format(total,other,self.__denominator)
                    
        return "{}/{}".format(self.__numerator, self.__denominator)
    
    def __mul__(self,other):
        if type(other) is type(self):
            return Fraction(self.get_num()*other.get_num(),self.get_den()*other.get_den())
        elif type(other) is type(1):
            return Fraction(self.get_num() * other,self.get_den())
        elif type(other) is type(.1):
            p, q = float_2_frac(other)
            return Fraction(self.get_num() * p, self.get_den() * q)
        else:
            raise TypeError("Unsupported type for operation.")

    def __rmul__(self,other):
        if type(other) is type(self):
            return self * other
        elif type(other) is type(1):
            return self * other
        elif type(other) is type(.1):
            p, q = float_2_frac(other)
            return Fraction(self.get_num() * p, self.get_den() * q)
        else:
            raise TypeError("Unsupported type for operation.")
        
    def __add__(self,other):
        if type(other) is type(self):
            r = gcd(self.get_den(), other.get_den())
            if r == 1:
                return Fraction(self.get_num() * other.get_den() + other.get_num() * self.get_den(), self.get_den() * other.get_den())
            else:
                t = self.get_num() * (other.get_den() // r) + other.get_num() * (self.get_den() // r)
                s = gcd(t, r)
                return Fraction( t // s, (self.get_den() // r) * (other.get_den() // s))
            
        elif type(other) is type(1):
            return Fraction(self.get_num() + self.get_den() * other, self.get_den())
        
        elif type(other) is type(.1):
            other=Fraction(*float_2_frac(other))
            r = gcd(self.get_den(), other.get_den())
            if r == 1:
                return Fraction(self.get_num() * other.get_den() + other.get_num() * self.get_den(), self.get_den() * other.get_den())
            else:
                t = self.get_num() * (other.get_den() // r) + other.get_num() * (self.get_den() // r)
                s = gcd(t, r)
                return Fraction( t // s, (self.get_den() // r) * (other.get_den() // s))
        else:
            raise TypeError("Unsupported type for operation.")
            

    
    def __radd__(self, other):
        if type(other) in (type(self),type(1),type(.1)):
            return self + other
        else:
            raise TypeError("Unsupported type for operation.")
    
    def __truediv__(self, other):
        if type(other) is type(self):
            return self * Fraction(other.get_den(), other.get_num())
        elif type(other) is type(1):
            return self * Fraction(1, other)
        elif type(other) is type(.1):
            q, p = float_2_frac(other)
            return self * Fraction(p, q)
        else:
            raise TypeError("Unsupported type for operation.")
    
    def __rtruediv__(self, other):
        if type(other) is type(self):
            return other / self
        elif type(other) is type(1):
            rev_frac = (self.get_den(), self.get_num())
            return other * Fraction(*rev_frac)
        elif type(other) is type(.1):
            rev_frac = (self.get_den(), self.get_num())
            return other * Fraction(*rev_frac)
        else:
            raise TypeError("Unsupported type for operation.")

    def __sub__(self, other):
        if type(other) in (type(self), type(1), type(.1)):
            return self + (other * -1)
        else:
            raise TypeError("Unsupported type for operation.")

    def __rsub__(self, other):
        if type(other) in (type(self), type(1), type(.1)):
            return other + (self * -1)
        else:
            raise TypeError("Unsupported type for operation.")

    def __gt__(self, other):
        if type(other) is type(self):
            den = lcm(self.get_den(), other.get_den())
            s_num = den // self.get_den() * self.get_num()
            o_num = den // other.get_den() * other.get_num()
            if s_num > o_num:
                return  True
            else:
                return False
        elif type(other) is type(1):
            if self.__numerator / self.__denominator > other:
                return True
            else:
                return False
        elif type(other) is type(.1):
            other = Fraction(*float_2_frac(other))
            den = lcm(self.get_den(), other.get_den())
            s_num = den // self.get_den() * self.get_num()
            o_num = den // other.get_den() * other.get_num()
            if s_num > o_num:
                return  True
            else:
                return False
        else:
            raise TypeError("Unsupported type for operation.")

    def __lt__(self, other):
        if type(other) is type(self):
            den = lcm(self.get_den(), other.get_den())
            s_num = den // self.get_den() * self.get_num()
            o_num = den // other.get_den() * other.get_num()
            if s_num < o_num:
                return  True
            else:
                return False
        elif type(other) is type(1):
            if self.__numerator / self.__denominator < other:
                return True
            else:
                return False
        elif type(other) is type(.1):
            other = Fraction(*float_2_frac(other))
            den = lcm(self.get_den(), other.get_den())
            s_num = den // self.get_den() * self.get_num()
            o_num = den // other.get_den() * other.get_num()
            if s_num < o_num:
                return  True
            else:
                return False
        else:
            raise TypeError("Unsupported type for operation.")

    
    def __eq__(self, other):
        if type(other) is type(self):
            if self.get_den() == other.get_den() and self.get_num() == other.get_num():
                return True
            else:
                return False
        elif type(other) is type(1):
            if self.get_den() != 1:
                return False
            if self.get_num() != other:
                return False
            else:
                return True
        elif type(other) is type(.1):
            other = Fraction(*float_2_frac(other))
            if self.get_den() == other.get_den() and self.get_num() == other.get_num():
                return True
            else:
                return False
        else:
            raise TypeError("Unsupported type for operation.")
        
    def __ne__(self, other):
        if type(other) in (type(self), type(1), type(.1)):
            if self == other:
                return False
            else:
                return True
        else:
            raise TypeError("Unsupported type for operation.")
    
    def __ge__(self, other):
        if type(other) in (type(self), type(1), type(.1)):
            if self > other or self == other:
                return True
            else:
                return False
        else:
            raise TypeError("Unsupported type for operation.")
    
    def __le__(self, other):
        if type(other) in (type(self), type(1), type(.1)):
            if self < other or self == other:
                return True
            else:
                return False
        else:
            raise TypeError("Unsupported type for operation.")
        


    def get_num(self):
        return self.__numerator


    def get_den(self):
        return self.__denominator




def main():
    """Return examples of using module frac."""
    print("Testing\n")
    x = Fraction(2, 7)
    y = Fraction(3, 2)
    z = Fraction(3, 4)
    t = Fraction(12, 8)
    u = Fraction(4, 10)
    l = Fraction(12, 30)
    print("14/8 = ",Fraction(14, 8))
    print(y ,"*", x, "=", y * x)
    print(x, "+", y, "=", x + y)
    print(z, "+", t, "=", z + t)
    print(x, "+", 8, "=", x + 8)
    print(x, "*", 3, "=", x * 3)
    print(Fraction(2, 9), "/", Fraction(1, 7), "=", Fraction(2, 9) / Fraction(1, 7))
    print(x, "-", y, "=", x - y)
    print(3, "-", t, "=", 3 - t)
    print(x, ">", y, "is", x > y)
    print("4/10", "=", "12/30", "is", u == l)
    print(u, "<", z, "is", u < z)
    print(x, "!=", y, "is", x != y)
    print(x, "<=", y, "is", x <= y)
    print("2/-5 < 3/21 is", Fraction(2, -5) < Fraction(3, 21))
    print("-8/-2", "=", 4, "is", Fraction(-8, -2) == 4)
    print("Denominator of ",x," : ",x.get_den())
    Fraction.enhanced = True
    print(Fraction(2.1,3))
    print(Fraction(3.25))
    Fraction.mixed = True
    print(Fraction(3,2))
    print(Fraction(11,22))
    Fraction.enhanced = False
    print(Fraction(3))
    print(Fraction(3.25))



if __name__ == "__main__":
    main()