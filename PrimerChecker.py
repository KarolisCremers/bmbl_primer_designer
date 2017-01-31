import re


_check_methods = "dimer", "hairpin", "self_dimer"


class PrimerChecker(object):
    """ The PrimerChecker object will check dimers, self dimers and
    hairpins determined by the parameters in the constructor. These
    are all experimental since it is string based and DOES NOT
    CALCULATE the Gibbs free energy which usually is done.
    Every method depends is_dimer, however when the dimer check is
    disabled this will not effect the result of self dimers or
    hairpins. This is done through the python magic method
    `__getattribute__` and an internal variable called
    `_internal_override`
    This class also contains utility methods to check primers, for
    instance `calc_primer_details`
    """

    complement_dict = dict(A='T', T='A', C='G', G='C')

    def __init__(self, required_bonds=6, dimer=True, self_dimer=True,
                 hairpin=True):
        """ This method will configure whether methods are enabled
        (True) or disabled (False). When a method is disabled, the
        method will always return True to ensure all checks pass
        and the using code has not to worry about this configuration.

        Parameters:
            required_bonds - The amount of bonds that are required to
            invalidate a dimer, self dimer or hairpin.
            dimer - Enables or disables `is_dimer`
            self_dimer - Enables or disables `is_self_dimer`
            hairpin -  - Enables or disables `hairpin`
        Returns:
            -
        """
        self.required_bonds = required_bonds
        self.check_dimer = dimer
        self.check_self_dimer = self_dimer
        self.check_hairpin = hairpin
        self._internal_override = False

    def check_bonds(self, primer_a, primer_b):
        """ Checks whether the two sequences can are bound together and
        are strong enough to actually invalidate the sequences. This
        means that required_bonds from the constructor is used.

        Parameters:
            primer_a - A sequence WITHOUT spaces
            primer_b - A sequence with or without spaces
        Returns:
            True when the sequences should be invalidated and False
            when it is valid
        """
        bonds = 0
        for i in range(len(primer_a)):
            if self.complement_dict[primer_a[i]] == primer_b[i]:
                bonds += 1
            if bonds == self.required_bonds:
                return True
        return False

    def calc_primer_details(self, primer):
        """ Calculates the melting temperature and GC% of a primer which
        has a length less than 25 nucleotides.

        Parameters:
            primer - The primer to check for
        Returns:
            1. The GC percentage
            2. The melting temperature
            This is a tuple.
        """
        gc_length = len(re.findall('[GC]', primer))
        # Calculate the GC%
        gc_perc = (float(gc_length) / len(primer)) * 100
        # Calculate the melting temp
        melting_temp = 4 * gc_length + 2 * (len(primer) - gc_length)
        return gc_perc, melting_temp

    def is_dimer(self, primer_a, primer_b):
        """ Checks whether primer_a and primer_b can form a dimer based
        on the required_bonds setting in the constructor. The largest
        primer always should not have spaces embedded in the string,
        otherwise KeyErrors will be thrown. In the case of equal length
        primers, the first primer (primer_a) is picked to be the "large"
        primer. This behaviour is used in `is_hairpin`
        This method will move the small primer along the large primer,
        so every possibility is accounted for.

        Parameters:
            primer_a - A primer containing no spaces
            primer_b - A primer of any length which may contain primers
        Returns:
            Whether the two primers can form a dimer (True) or not
            (False).
        """
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
        """ This will check whether the primer can form a dimer with
        another primer of the same type. This means that a check is
        made whether the forward primer can form a dimer with another
        forward primer. This is also goes for the reverse primer with
        the reverse primer.

        Parameters:
            primer - The primer to do the self dimer check on
        Returns:
            Whether the primer can form a self dimer (True) or not
            (False).
        """
        self._internal_override = True
        output = self.is_dimer(primer, primer)
        self._internal_override = False
        return output

    def is_hairpin(self, primer):
        """ Checks whether the primer can form a hairpin.

        Parameters:
            primer - The primer to do the hairpin check on
        Returns:
            Whether the primer can form a hairpin (True) or not (False)
        """
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
        """ This is a 'magic method' in python and should not be called
        directly unless a child class needs the super form.
        Refer for this method to: http://bit.ly/2ja7BKM
        This method handles whether a method should be called in the
        first place defined by the dimer, self_dimer and hairpin
        settings in the constructor.
        This is done because the method `is_dimer` is both used by
        `is_self_dimer` and `is_hairpin.`
        This check is done when only when the variable
        `_internal_override` is False and the configuration variable
        is also False.

        Parameters:
            key - The attribute which needs to be returned
        Returns:
            The correct attribute, or true when a check should not be
            done.
        """
        if key[3:] in _check_methods:
            if (not self._internal_override and
                    not getattr(self, "check_" + key[3:])):
                return lambda *x: False
        return super(PrimerChecker, self).__getattribute__(key)
