from basex import num_to_seq, seq_to_num
from utils import cint, max_idx, stack, trim

def cube0(b, d):
    return d-1-b

def direct(b, d):
    return b%d

def pm2iplus0(b, d):
    # PM2I+0
    return (b+1) % d

def _build_layer(n, bases, direct, overlay, augment, exchange_func, next_base):
    # Build the shuffle layer
    shuffle = []
    for x in xrange(n):
        xseq = num_to_seq(x, bases)
        out = set()
        # if direct is set, point to itself
        # otherwise, <<1, shuffle = Exchange(Omega(X, 1))
        # if overlay is set, do it for LogN times
        for k in xrange(0 if direct else 1, len(bases) if overlay else 2):
            shifted_bases = bases[-k:] + bases[:-k]
            yseq =  [exchange_func(b, d) for b, d in zip(xseq[-k:], bases[-k:])] + xseq[:-k]  # Exchange(x<<k)
            if augment:
                # connect to every node in a block
                out.update([seq_to_num([i] + yseq[1:], shifted_bases) for i in xrange(shifted_bases[0])])
            else:
                # just add one node in a block
                out.add(seq_to_num(yseq, shifted_bases))
        shuffle.append(list(out))

    # Build the switcher layer
    shifted_bases = bases[-1:] + bases[:-1]
    switcher = []
    num_blocks = reduce(lambda x, y: x*y, shifted_bases[1:], 1)
    blocks = [[[range(next_base)] * shifted_bases[0]]] * num_blocks
    switcher = stack(*blocks)[0]

    return [shuffle, switcher]


def mn(m, n, num_layers=2, direct=False, overlay=False, augment=False, exchange_func=pm2iplus0):
    assert num_layers >= 1
    # num_layers == 1 means fully connected NN
    bases = [cint(m ** (1./num_layers))] * num_layers
    k = m

    result = []
    for i in range(num_layers):
        next_base = cint(bases[-1] * ((n*1./k) ** (1./(num_layers-i))))
        # print "[n%d][k%d][num_layers%d][i%d][next_base%d]" % (n, k, num_layers, i, next_base)
        # print "BASES: ", bases
        layer = _build_layer(k, bases, direct, overlay, augment, exchange_func, next_base)
        result.extend(layer)
        k = max_idx(layer[1])
        bases = [next_base] + bases[:-1]

    return result
