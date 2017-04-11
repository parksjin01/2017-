import cPickle

with open('test', 'rb') as f:
    data = cPickle.load(f)
print data[4]