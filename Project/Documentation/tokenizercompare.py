
import happyfuntokenizing
from twokenize import simpleTokenize

print "token test"
tokenizer = happyfuntokenizing.Tokenizer(preserve_case=False)

for x in xrange(1, 10):
    print "---- ARK ----------"
    print simpleTokenize(tweets["pos"][x].text)
    
    print "---- HappyFun -----"
    print tokenizer.tokenize(tweets["pos"][x].text)