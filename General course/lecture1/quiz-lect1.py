class Rational():
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator)
    def reduce(self, n):
        if (self.numerator % n)==0 and (self.denominator % n)==0:
            self.numerator /= n
            self.denominator /= n
