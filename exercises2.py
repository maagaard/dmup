import test
from collections import OrderedDict

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

def group_count(list_char):
    resDict = {}
    for c in list_char:
        resDict[c] = resDict.get(c, 0) + 1
    return resDict
# def test_is_harshad():
#     return False
    
test_is_harshad()
test_split_digits()

def factorial(n):
    return n * factorial(n-1) if n > 0 else 1
        
def factorial2(n):
    return reduce(lambda x,y: x*y, range(1,n+1))


class SortedKeysDict(dict):

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)  # use the free update to set keys
        sorted_keys = sorted(self)
        new_dict = collections.OrderedDict()
        for key in sorted_keys:
            new_dict[key] = self[key]

        print new_dict.keys()
        
        self = new_dict


        # self = sorted(self)
        

    # def __init__(self, dict):
    #     self.items = dict




