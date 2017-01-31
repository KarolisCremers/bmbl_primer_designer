from PrimerFinder import PrimerFinder
import time


class TargetPrimerFinder(PrimerFinder):

    def __init__(self, primer_checker, sequence, anneal_minimum,
                 anneal_maximum, max_pcr_product, target_minimum,
                 target_maximum):
        super(TargetPrimerFinder, self).__init__(
            primer_checker, sequence, anneal_minimum, anneal_maximum,
            max_pcr_product)
        self.target_minimum = target_minimum - anneal_minimum
        self.target_maximum = target_maximum - anneal_minimum

    def find_primers(self):
        sequence = self.get_annealing_sequence()
        forward_primer_region, reverse_primer_region = (
            self.find_primer_region(sequence, self.target_minimum,
                                    self.target_maximum))
        forward_primers = self.primer_search(forward_primer_region)
        reverse_primers = self.primer_search(reverse_primer_region)
        primer_pairs = []
        for forward_primer in forward_primers:
            position_forward = forward_primer["offset"]
            for reverse_primer in reverse_primers:
                if self.primer_checker.is_dimer(forward_primer['seq'],
                                                reverse_primer['seq']):
                    continue
                rprimer = dict(reverse_primer)
                rprimer["seq"] = rprimer["seq"][::-1]
                position_reverse = reverse_primer["offset"]
                pcr_product = ((len(sequence) - position_reverse) -
                                position_forward)
                if pcr_product <= self.max_pcr_product:
                    primer_pairs.append(
                        dict(fprimer=forward_primer, rprimer=rprimer,
                             pcr=sequence[position_forward:position_forward +
                                          pcr_product]))
        primer_pairs.sort(key=lambda i: len(i["pcr"]))
        return primer_pairs[0] if primer_pairs else None

    def primer_search(self, primer_region):
        primers = []
        primer_length = 17
        while primer_length <= 30:
            for position in range(0, len(primer_region)):
                primer_seq = primer_region[position:(position + primer_length)]
                gc_percentage, melt_temperature = (
                    self.primer_checker.calc_primer_details(primer_seq))
                if (50 <= gc_percentage <= 60 and
                    55 <= melt_temperature <= 65 and
                    not self.primer_checker.is_hairpin(primer_seq) and
                    not self.primer_checker.is_self_dimer(primer_seq)):
                    primers.append(dict(offset=position, seq=primer_seq,
                                        gc_perc=gc_percentage,
                                        melt_temp=melt_temperature))
            primer_length += 1
        return primers

    def find_primer_region(self, input_sequence, target_minimum,
                           target_maximum):
        '''
        :param input_sequence is the annealing sequence:
        :param target_minimum is the start position of the target
        sequence in the annealing sequence:
        :param target_maximum is the end position of the target
        sequence in the annealing sequence:
        In this function are the primer regions ,wherein the primers
        can be found, created by taking the
        :return:
        '''
        reverse_sequence = self.complement_sequence(input_sequence)
        forward_primer_region = input_sequence[:target_minimum + 17]
        reverse_primer_region = reverse_sequence[:(len(
            input_sequence) - target_maximum)]
        return forward_primer_region, reverse_primer_region

