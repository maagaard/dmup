import test
import pytest.mark.randomize

def is_harshad(n):
    return (n % sum(split_digits(n))) == 0
    
def split_digits(n):
    res = []
    while n != 0:
        m = n%10
        res.append(m)
        n /= 10
    return res
    
def is_harshad2(n):
    return (n % (sum(map(int, str(n))))) == 0

def test_split_digits():
    assert split_digits(123) == [3,2,1]
    assert split_digits(591239) == [9,3,2,1,9,5]

def test_is_harshad():
    return False
    
