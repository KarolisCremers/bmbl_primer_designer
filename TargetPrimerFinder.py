    from PrimerFinder import PrimerFinder

    class TargetPrimerFinder(PrimerFinder):

        def __init__(self, primer_checker, sequence, anneal_minimum,
                     anneal_maximum, max_pcr_product, target_minimum,
                     target_maximum):
            super(TargetPrimerFinder, self).__init__(
                primer_checker, sequence, anneal_minimum, anneal_maximum,
                max_pcr_product)
            self.target_minimum = target_minimum
            self.target_maximum = target_maximum

        def find_primers(self):
            # Dit is de hoofdfunctie waar je kan beginnnen
            # Je hoeft je geen zorgen te maken over de annealing sequence
            sequence = self.get_annealing_sequence()

            # Het controloren van dimeren en dergelijke kan je doen door
            # de functies:
            #   self.primer_checker.is_dimer(a, b)
            #   self.primer_checker.is_self_dimer(a)
            #   self.primer_checker.is_hairpin(a)

            # Het opvragen van gc_perc en smelt temp:
            #   self.primer_checker.calc_primer_details(a)

            # Het flippen van een nucleotide sequentie:
            #   self.complement_sequence(seq)
            #   Je krijgt dan je complement 3' -> 5'
            #   self.complement_sequence(seq, False)
            #   Je krijgt dan je complement 5' -> 3'

            # Verder heb je toegang tot de variabelen in de __init__, alleen
            # wordt dat in de super class gedaan
