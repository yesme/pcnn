from basex import num_to_seq, seq_to_num
from utils import cint, max_idx

def mn(m, n, num_layers=2, overlay=False):
    assert num_layers >= 1
    bases = [cint(m ** (1./num_layers))] * num_layers
    k = m

    result = []
    for i in range(num_layers):
        layer = []
        next_base = cint(bases[i] * ((n*1./k) ** (1./(num_layers-i))))
        next_bases = bases[:i] + [next_base] + bases[i+1:]
        for x in xrange(reduce(lambda x, y: x*y, bases, 1)):
            xseq = num_to_seq(x, bases)
            if not overlay:
                out = set([seq_to_num(xseq[:i] + [j] + xseq[i+1:], next_bases) for j in xrange(next_bases[i])])
            else:
                out = set([seq_to_num(xseq[:l] + [j] + xseq[l+1:], next_bases) for l in xrange(num_layers) for j in xrange(next_bases[l])])
            layer.append(list(out))
        k = max_idx(layer)
        bases = next_bases
        result.append(layer)

    return result
