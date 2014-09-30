
def func(x,a,b,c):
    return c-x*b/(x+a)
popt,pcov=curve_fit(func,ppfd,nee)
print popt
# except:
#     print "Unexpected error:", sys.exc_info()[0]
# else:
#     print "done with no exceptions"
print time.clock()-ticks
