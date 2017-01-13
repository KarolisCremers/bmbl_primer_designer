from re import split


class PrimerFinder(object):

    def __init__(self, primer_checker, sequence, anneal_minimum,
                 anneal_maximum, max_pcr_product):
        self.primer_checker = primer_checker
        self.sequence = "".join(split("\s+", sequence.upper()))
        self.anneal_minimum = anneal_minimum
        self.anneal_maximum = anneal_maximum
        self.max_pcr_product = max_pcr_product

    def complement_sequence(self, sequence, flip_sequence=True):
        complement_dict = dict(A='T', T='A', C='G', G='C')
        complement_seq = ""
        if flip_sequence:
            sequence = reversed(seqeunce)
        for nucleotide in sequence:
            complement_seq += complement_dict[nucleotide]
        return complement_seq

    def get_annealing_sequence(self):
        return self.sequence[self.anneal_minimum - 1:self.anneal_maximum - 1]

    def find_primers(self):
        raise NotImplementedError
