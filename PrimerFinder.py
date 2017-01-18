from re import split


class PrimerFinder(object):
    """ This is a baseclass which handles the settings of a complete
    input from the input and modifies the sequence to make sure it
    is upper case. This is already done in the GUI, but this is a
    standalone class and should also do it.
    The method `find_primers` should be considered as a main method.
    This should return a list of results which look like the
    following structure:
    TODO
    """

    def __init__(self, primer_checker, sequence, anneal_minimum,
                 anneal_maximum, max_pcr_product):
        """ The constructor of this class which initialises the
        input variables. Only the sequence is converted to uppercase
        and removes all whitespace from it.

        Parameters:
            primer_checker - A PrimerChecker object which handles the
            checks for dimers, self dimers and hairpins (experimentally)
            sequence - The sequence of nucleotides where primers need to
            be found in.
            anneal_minimim - Determines the minimum of the range of the
            actual sequence which primers are allowed to anneal to.
            anneal_maximum - Determines the maximum of the range of the
            actual sequence which primers are allowed to anneal to.
            max_pcr_product - Determines the length of the maximal
            final PCR product.
        Returns:
            -
        """
        self.primer_checker = primer_checker
        self.sequence = "".join(split("\s+", sequence.upper()))
        self.anneal_minimum = anneal_minimum
        self.anneal_maximum = anneal_maximum
        self.max_pcr_product = max_pcr_product

    def complement_sequence(self, sequence, flip_sequence=True):
        """ Creates the complement of a given sequence.

        Parameters:
            sequence - The sequence to make the complement of.
            flip_sequence - Determines whether to make the complement
            from 3' to 5' (True) or 5' to 3'.
        Returns:
            The complement of the given sequence in the correct
            orientation determined by flip_sequence.
        """
        complement_dict = dict(A='T', T='A', C='G', G='C')
        complement_seq = ""
        if flip_sequence:
            sequence = reversed(sequence)
        for nucleotide in sequence:
            complement_seq += complement_dict[nucleotide]
        return complement_seq

    def get_annealing_sequence(self):
        """ Retrieves the sequence which primers can anneal to. Uses
        anneal_minimum and anneal_maximum from the constructor.

        Parameters:
            -
        Returns:
            The sequence which primers can anneal to.
        """
        return self.sequence[self.anneal_minimum - 1:self.anneal_maximum - 1]

    def find_primers(self):
        """ The main method which searches for the primers for this class """
        raise NotImplementedError
