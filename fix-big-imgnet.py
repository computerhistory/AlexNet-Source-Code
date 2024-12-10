import os
import sys
from PIL import Image
from StringIO import StringIO
from util import *

src = '/ais/gobi3/u/ilya/jpg_valid_2010_85/'
dst = '/ais/gobi3/u/kriz/lsvrc-2010-jpg/'

BATCH_SIZE = 1024

def save_batch(c_strings, c_labels, c_wnids, out_b):
    pickle(os.path.join(dst, 'data_batch_%d' % out_b), (c_strings, c_labels, c_wnids))

    return out_b + 1
if __name__ == "__main__":
    c_strings = []
    c_labels = []
    c_wnids = []
    out_b = 2000
    for b in xrange(49):
        failed = 0
        strings, sizes, labels = unpickle(os.path.join(src, '%s' % b))
        for s,l in zip(strings, labels):
            try:
                im = Image.open(StringIO(s)).convert('RGB')
                c_strings += [s]
                c_labels += [l[1]]
                c_wnids += [l[0]]
                if len(c_strings) == BATCH_SIZE:
                    out_b = save_batch(c_strings, c_labels, c_wnids, out_b)
                    c_strings = []
                    c_labels = []
                    c_wnids = []
            except IOError,e:
                failed += 1
        print "Batch %d failed: %d" % (b, failed)
            
    if len(c_strings) > 0:
        save_batch(c_strings, c_labels, c_wnids, out_b)
