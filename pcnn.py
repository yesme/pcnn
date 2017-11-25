import clos
import kcube
import omega
import utils

M = 4096
N = 1024

# network = omega.mn(M, N, num_layers=2, direct=False, overlay=False, augment=False, exchange_func=omega.direct)
# network = kcube.mn(M, N, num_layers=3, overlay=False)
network = clos.mn(M, N, 3, strict_nonblocking=True)
utils.info(network)
# print network
network = utils.trim(network, M, N)
utils.info(network)
# print network
