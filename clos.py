from functools import partial
import unittest

from scipy import optimize as opt

from utils import cint, rint, stack

# optimal results can be found: http://www.scialert.net/fulltext/?doi=jas.2008.4234.4237
# our case is slightly different - the connections between stages should be considered too.
# [note] since this n1 and n2 are optimization, we use round instead of ceiling.
def _get_links_strict(M, N, n):
    # strictly non-blocking
    n1, n2 = n
    res = (n1+n2-1)*(M+N+M/n1+N/n2+(M*N)/(n1*n2))
    return res

def _get_links_rearrangeable(M, N, n):
    # rearrangeable non-blocking
    n1, n2 = n
    res = max(n1, n2)*(M+N+M/n1+N/n2+(M*N)/(n1*n2))
    return res

def _solve(M, N, strict_nonblocking=False):
    if strict_nonblocking:
        target = partial(_get_links_strict, M, N)
    else:
        target = partial(_get_links_rearrangeable, M, N)
    mid = (M*N*1./(M+N))**.5
    b0 = .5 * min(M, N)**.5
    b1 = 2. * max(M, N)**.5
    n1, n2 = opt.minimize(target, (mid, mid), bounds=((b0,b1), (b0,b1))).x
    # print "%.3f %.3f" % (n1, n2)
    n1 = rint(n1)
    n2 = rint(n2)
    return n1, n2

def _xlink(m, n):
    # n groups of m inputs cross link to m groups of n outputs
    return [[j*n+i] for i in xrange(n) for j in xrange(m)]

def mn(m, n, stages=3, strict_nonblocking=False, augment=False):
    assert stages % 2 == 1
    if stages == 1:
        # return mxn full connection
        return [[range(n)] * m]

    # otherwise, build the network recursively
    n1, n2 = _solve(m, n, strict_nonblocking)
    k = (n1+n2-1) if strict_nonblocking else max(n1, n2)
    r1 = cint(m*1./n1)
    r2 = cint(n*1./n2)
    layers = []

    # Build the first stage
    blocks = [[[range(k)] * n1]] * r1
    layers.extend(stack(*blocks))

    # Connect the first stage with the core switch network
    layers.append(_xlink(r1, k))

    # Recursively build the core switch network
    blocks = [mn(r1, r2, stages-2, strict_nonblocking)] * k
    layers.extend(stack(*blocks))

    # Connect the core switch network with the last stage
    layers.append(_xlink(k, r2))

    # Build the last stage
    blocks = [[[range(n2)] * k]] * r2
    layers.extend(stack(*blocks))

    return layers

class TestBaseXMethods(unittest.TestCase):

    def test_crosslink(self):
        self.assertEqual(
            _xlink(3, 2),
            [[0], [2], [4], [1], [3], [5]])


if __name__ == '__main__':
    unittest.main()