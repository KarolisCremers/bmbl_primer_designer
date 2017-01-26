import re


_check_methods = "dimer", "hairpin", "self_dimer"


class PrimerChecker(object):
    complement_dict = dict(A='T', T='A', C='G', G='C')

    def __init__(self, required_bonds=3, dimer=True, self_dimer=True,
                 hairpin=True):
        self.required_bonds = required_bonds
        self.check_dimer = dimer
        self.check_self_dimer = self_dimer
        self.check_hairpin = hairpin
        self._internal_override = False

    def check_bonds(self, primer_a, primer_b):
        bonds = 0
        for i in range(len(primer_a)):
            if self.complement_dict[primer_a[i]] == primer_b[i]:
                bonds += 1
            if bonds == self.required_bonds:
                return True
        return False

    def calc_primer_details(self, primer):
        ''' Calculates the melting temperature and GC% of a primer which
        has a length less than 25 nucleotides.
        '''
        gc_length = len(re.findall('[GC]', primer))
        # Calculate the GC%
        gc_perc = (float(gc_length) / len(primer)) * 100
        # Calculate the melting temp
        melting_temp = 4 * gc_length + 2 * (len(primer) - gc_length)
        return gc_perc, melting_temp

    def is_dimer(self, primer_a, primer_b):
        # Assume primers dont have whitespace and are uppercase
        large_primer = primer_a if len(primer_a) >= len(primer_b) else primer_b
        small_primer = primer_b if large_primer == primer_a else primer_a
        # Move the smallest primer along the larger primer
        start_index = len(small_primer) - self.required_bonds
        end_index = start_index + len(large_primer)
        moving_primer = (small_primer +
                         (" " * (len(large_primer) - self.required_bonds)))
        for _ in range(len(moving_primer) - self.required_bonds):
            if self.check_bonds(large_primer,
                                moving_primer[start_index:end_index]):
                return True
            moving_primer = " " + moving_primer[:-1]
        return False

    def is_self_dimer(self, primer):
        self._internal_override = True
        output = self.is_dimer(primer, primer, required_bonds)
        self._internal_override = False
        return output

    def is_hairpin(self, primer):
        if len(primer) < self.required_bonds * 2:
            return False
        self._internal_override = True
        for i in range(self.required_bonds + 1, len(primer)):
            a = primer[:i - 1]
            b = primer[i + 1:]
            len_difference = abs(len(a) - len(b))
            full = a if len(a) > len(b) else b
            padded = (" " * len_difference) + (b if full == a else a)
            if self.is_dimer(full, padded):
                self._internal_override = False
                return True
        self._internal_override = False
        return False

    def __getattribute__(self, key):
        if key[3:] in _check_methods:
            if (not self._internal_override and
                    not getattr(self, "check_" + key[3:])):
                return lambda *x: False
        return super(PrimerChecker, self).__getattribute__(key)
