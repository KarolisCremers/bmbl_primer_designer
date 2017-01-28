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
        while len(sequence[offset:]) >= offset + 17:
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

    def link_primers(self, primer_list):
        """ Tries to find all forward primer, reverse primer
        combinations. When those reverse primers are found for a
        forward primer, a few checks will be done by the
        range_primer_filter. Those links are only added when actual
        links between a forward primer and reverse primer exist.

        Parameters:
            primer_list - A list of available primers.
        Returns:
            A list of dictionaries with all the link dictionaries. The
            primer key is the forward primer and the rprimers key is a
            list of reverse primers.
        """
        links = []
        for _ in range(0, len(primer_list)):
            link = dict(primer=primer_list[0])
            del primer_list[0]

            link['rprimers'] = list(
                filter(self.range_primer_filter(link['primer']),
                       primer_list))
            # Only when primers are available, add it to the links
            if link['rprimers']:
                links.append(link)
        return links

    def set_primer_absolute_position(self, primer_obj):
        """ Calculates the absolute position for a primer object.
        Parameters:
            primer_obj - The primer obj to calculate for.
        Returns:
            A tuple with the start and end integer.
        """
        start = self.anneal_minimum + primer_obj['offset'] + 1
        end = start + len(primer_obj['seq'])
        primer_obj['position'] = start, end
        del primer_obj['offset']
        return start, end

    def find_primers(self):
        sequence = self.get_annealing_sequence()
        linked_primers = self.link_primers(self.find_all_primers(sequence))
        for linked in linked_primers:
            self.set_primer_absolute_position(linked['primer'])
            start_position = linked['primer']['position'][0]
            for i in range(0, len(linked['rprimers'])):
                # Hard copy
                primer = linked['rprimers'][i] = dict(linked['rprimers'][i])
                primer['seq'] = self.complement_sequence(primer['seq'], False)
                _, end = self.set_primer_absolute_position(primer)
                primer['pcr'] = self.sequence[start_position:end]
        return linked_primers
