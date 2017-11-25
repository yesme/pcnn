import math

def max_idx(layer):
    return max([idx for node in layer if node for idx in node]) + 1

def cint(f):
    return int(math.ceil(f))

def rint(f):
    return int(f+0.5)

def info(network):
    num_edges = sum([len(node) for layer in network for node in layer])
    m = len(network[0])
    n = max_idx(network[-1])
    print "This [%sx%d] Network has [%d] edges on [%d] layers, [%.2f%%] of total edges." % (
        "x".join(["%d"%len(l) for l in network]), n, num_edges, len(network), num_edges*100.0/(m*n))

def trim(network, m, n, padding=False):
    # Two passes: forward and backward
    # forward pass
    pass_one = []
    valids = set(range(m))
    for layer in network:
        new_layer = [node if i in valids else [] for i, node in enumerate(layer)]
        valids = set([_ for node in new_layer for _ in node])
        pass_one.append(new_layer)

    # backward pass
    pass_one.reverse()
    pass_two = []
    valids = sorted(valids)[:n]
    mappings = {v: idx for idx, v in enumerate(valids)}
    for layer in pass_one:
        new_layer = [(i, [mappings[x] for x in node if x in mappings]) for i, node in enumerate(layer)]
        new_layer = [(i, node) for i, node in new_layer if node]
        mappings = {v[0]: idx for idx, v in enumerate(new_layer)}
        pass_two.append([node for i, node in new_layer])
    pass_two.reverse()

    if padding:
        first = len(pass_two[0])
        pass_two[0] += [[]] * (m-first)

    return pass_two

def stack(*networks):
    # verify if all the networks have the same number of layers
    layers = set([len(network) for network in networks])
    assert len(layers) is 1
    layers = layers.pop()

    # padding the networks

    # stack each layer
    result = []
    for layer in zip(*networks):
        offset = 0
        nodes = []
        for subnet in layer:
            width = max_idx(subnet)
            nodes.extend([map(lambda x: x+offset, node) for node in subnet])
            offset += width
        result.append(nodes)
    return result

def reverse(network):
    result = []
    for layer in network:
        max_idx = max_idx(layer)
        output = [[] for _ in range(max_idx)]
        for i, node in enumerate(layer):
            for idx in node:
                output[idx].append(i)
        result.append(output)
    result.reverse()
    return result
