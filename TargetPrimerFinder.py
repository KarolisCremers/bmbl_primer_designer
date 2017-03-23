from AllPrimerFinder import AllPrimerFinder


class TargetPrimerFinder(AllPrimerFinder):

    def __init__(self, primer_checker, sequence, anneal_minimum,
                 anneal_maximum, max_pcr_product, target_minimum,
                 target_maximum):
        super(TargetPrimerFinder, self).__init__(
            primer_checker, sequence, anneal_minimum, anneal_maximum,
            max_pcr_product)
        self.target_minimum = target_minimum - anneal_minimum
        self.target_maximum = target_maximum - anneal_minimum

    def range_primer_filter(self, forward_primer):
        super_check = (super(TargetPrimerFinder, self)
                       .range_primer_filter(forward_primer))
        start_forward = forward_primer["position"][0]

        def range_target_check(other):
            end_reverse = other["position"][1]
            if (start_forward < self.target_minimum
                    and end_reverse > self.target_maximum):
                return super_check(other)
            return False
        return range_target_check
