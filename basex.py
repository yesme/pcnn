import unittest

# Both bases and the output follows little-endian, which means
# the least significant digit is stored in seq[0].

def num_to_seq(num, bases):
    seq = []
    for base in bases:
        seq.append(num%base)
        num /= base
    assert num == 0, "%d cannot be represented in %d digits." % (num, len(bases))
    return seq

def seq_to_num(seq, bases):
    num = 0
    assert len(seq) == len(bases), "The length of sequence (%d) and bases (%d) doesnot match." % (len(seq), len(bases))
    for x, d in reversed(zip(seq, bases)):
        num *= d
        num += x
    return num


class TestBaseXMethods(unittest.TestCase):

    def test_same(self):
        num = 4319875465
        bases = [29, 13, 3, 11, 19, 2, 31, 17, 7, 23, 5]
        seq = num_to_seq(num, bases)
        res = seq_to_num(seq, bases)
        self.assertEqual(num, res)

    def test_base_too_short(self):
        num = 123456
        bases = [5, 7, 11]
        self.assertRaises(AssertionError, num_to_seq, num, bases)

    def test_seq_bases_doesnot_match(self):
        seq = [2, 0]
        bases = [5, 7, 11]
        self.assertRaises(AssertionError, seq_to_num, seq, bases)


if __name__ == '__main__':
    unittest.main()