from PrimerFinder import PrimerFinder


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
            position_forward = forward_primer[0]
            for reverse_primer in reverse_primers:
                position_reverse = reverse_primer[0]
                pcr_product = ((len(sequence) - position_reverse) -
                                position_forward)
                if pcr_product < max_pcr_product:
                    primer_pairs.append([pcr_product, forward_primer,
                                         reverse_primer])
        primer_pairs.sort()
        return primer_pairs

    def primer_search(self, primer_region):
        primers = []
        primer_length = 17
        while primer_length <= 30:
            for position in range(0, len(primer_region)):
                primer = []
                gc_percentage, \
                melt_temperature = self.primer_checker.calc_primer_details(
                    primer_region[:(position + primer_length)])
                primer.insert(position, 0)
                primer.append(gc_percentage)
                primer.append(melt_temperature)
                if 50 <= gc_percentage <= 60 and 55 <= melt_temperature <= 65:
                        primers.append(primer)
                primer_length += 1
        primers = sorted(primers)
        return primers

    def dimer_hairpin_checker(self, forward_primer, reverse_primer):
        cross_dimer = self.dimer_checker.is_dimer(forward_primer,
                                                  reverse_primer)
        self_dimer_forward = self.dimer_checker.is_self_dimer(
            forward_primer)
        self_dimer_reverse = self.dimer_checker.is_self_dimer(
            reverse_primer)
        hairpin_forward = self.dimer_checker.is_hairpin(forward_primer)
        hairpin_reverse = self.dimer_checker.is_hairpin(reverse_primer)
        if cross_dimer or self_dimer_forward or self_dimer_reverse or \
                hairpin_forward or hairpin_reverse:
            unvalid_primer = True
        else:
            unvalid_primer = False
        return unvalid_primer

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

