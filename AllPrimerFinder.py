from PrimerFinder import PrimerFinder


class AllPrimerFinder(PrimerFinder):

    def single_primer_filter(self, item):
        """ This filter will be used to filter out primers which are
        not capable of being a primer. A self dimer or hairpin is not
        allowed. The settings of experimental dimer checks are honoured
        through the PrimerChecker object.
        Parameters:
            item - The primer to check
        Returns:
            A boolean whether this primer can pass (True) or not(False)
        """
        primer = item["seq"]
        return (not self.primer_checker.is_self_dimer(primer) and
                not self.primer_checker.is_hairpin(primer))

    def range_primer_filter(self, forward_primer):
        """ This method will return to check a forward primer with
        multiple reverse primers. This method makes use of the closure
        principle to store information about the forward primer. See
        actual filter for details for what it is checking for.
        Parameters:
            forward_primer - The forward primer object
        Returns:
            A filter which takes a reverse primer as argument.
        """
        offset = forward_primer['offset']
        primer = forward_primer['seq']
        melt_temp = forward_primer['melt_temp']

        def reverse_primer_filter(other):
            """ This method will do a few checks on the forward and
            reverse primer:
            - Whether the max_pcr_product is within limits
            - Whether the primers do not overlap
            - Whether the melting temp is less or equal than 5
            - Whether the primers can form a dimer (in respect to the
              experimental setting)
            Parameters:
                other - The reverse primer object
            Returns:
                Whether the primers can be a good combination (True) or
                not (False)
            """
            pcr_product = other['offset'] - offset + len(other['seq'])
            melt_temp_difference = abs(other['melt_temp'] - melt_temp)
            return (pcr_product <= self.max_pcr_product and
                    len(primer) + offset < other['offset'] and
                    melt_temp_difference <= 5 and
                    not self.primer_checker.is_dimer(primer, other['seq']))

        return reverse_primer_filter

    def find_all_primers(self, sequence):
        """ This method will find all the primers in the sequence
        ranging in length from 17 to 30. There are also checks in place
        for duplicates (which then cannot be used) and the dimer checks
        using the single_primer_filter.

        Parameters:
            sequence - The sequence to look in
        Returns:
            A list of available primers
        """
        offset = 0
        found_primers = []
        primer_tracker = set()
        # Keep looping until we cannot find primers
        while len(sequence[offset:]) >= 17:
            current_region = sequence[offset:]
            offset += 1
            # check multiple primer lengths
            for primer_length in range(17, min(31, len(current_region))):
                primer = current_region[:primer_length]
                # Check for duplicates
                if primer in primer_tracker:
                    found_duplicates = []
                    for idx in range(len(found_primers)):
                        if found_primers[idx]["seq"] == primer:
                            found_duplicates.append(idx)
                    for idx in reversed(found_duplicates):
                        del found_primers[idx]
                    continue
                # Process the primer
                gc_perc, melting_temp = (
                    self.primer_checker.calc_primer_details(primer))
                if 50 <= gc_perc <= 60 and 55 <= melting_temp <= 65:
                    primer_tracker.add(primer)
                    found_primers.append(dict(seq=primer, gc_perc=gc_perc,
                                              melt_temp=melting_temp,
                                              offset=offset - 1))
        return list(filter(self.single_primer_filter, found_primers))

    def find_best_match(self, primers):
        """ Finds the best match of primers which have the biggest PCR product
        within the anneal region.

        Parameters:
            primer - A list of found primers
        Returns:
            A dictionary with the forward primer and reverse primer or None
            when no combination is found.
        """
        for _ in range(0, len(primers)):
            forward_primer = primers[0]
            del primers[0]
            primer_filter = self.range_primer_filter(forward_primer)
            for i in range(len(primers) - 1, -1, -1):
                rprimer = dict(primers[i])
                rprimer['seq'] = self.complement_sequence(rprimer['seq'])
                if primer_filter(rprimer):
                    return {'fprimer': forward_primer, 'rprimer': primers[i]}

    def find_primers(self):
        sequence = self.get_annealing_sequence()
        primers = self.find_all_primers(sequence)
        match = self.find_best_match(primers)
        if match:
            start_forward = (
                self.set_primer_absolute_position(match['fprimer'])[0])
            end_reverse = (
                self.set_primer_absolute_position(match['rprimer'])[1])
            match['pcr'] = self.sequence[start_forward:end_reverse]
            match['rprimer']['seq'] = self.complement_sequence(
                match['rprimer']['seq'], False)
        return match
