import sys
sys.path.insert(0, '../')
import debug



def test_dlog():
    print "Debug is: " + str(debug.DEBUG)
    debug.DLOG("This should only be vissible if debug is True")




def run_all():
    test_dlog()


if __name__ == '__main__':
    run_all()
