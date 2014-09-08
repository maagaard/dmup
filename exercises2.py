import test
# import pytest.mark.randomize

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
    assert is_harshad(81) == True
    assert is_harshad(55) == False
    assert is_harshad(99) == False
    assert is_harshad(54) == True
    assert is_harshad(23) == False
    assert is_harshad2(81) == True
    assert is_harshad2(55) == False
    assert is_harshad2(99) == False
    assert is_harshad2(54) == True
    assert is_harshad2(23) == False

# def test_is_harshad():
#     return False
    
test_is_harshad()
test_split_digits()
