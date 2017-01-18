from PrimerFinder import PrimerFinder


class AllPrimerFinder(PrimerFinder):

    def single_primer_filter(self, item):
        primer = item["seq"]
        return (self.primer_checker.is_self_dimer(primer) and
                self.primer_checker.is_hairpin(primer))

    def range_primer_filter(self, forward_primer):
        offset = forward_primer['offset']
        primer = forward_primer['seq']
        melt_temp = forward_primer['melt_temp']

        def reverse_primer_filter(other):
            pcr_product = other['offset'] - offset + len(other['seq'])
            melt_temp_difference = abs(other['melt_temp'] - melt_temp)
            return (pcr_product <= self.max_pcr_product and
                    len(primer) + offset < other['offset'] and
                    melt_temp_difference <= 5 and
                    not self.primer_checker.is_dimer(primer, other['seq']))

        return reverse_primer_filter

    def find_all_primers(self, sequence):
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
        links = []
        for _ in range(0, len(primer_list)):
            link = dict(primer=primer_list[0])
            del primer_list[0]

            link['end_primers'] = list(
                filter(self.range_primer_filter(link['primer']),
                       primer_list))
            # Only when primers are available, add it to the links
            if link['end_primers']:
                links.append(link)
        return links

    def find_primers(self):
        sequence = self.get_annealing_sequence()
        linked_primers = self.link_primers(self.find_all_primers(sequence))
        for linked in linked_primers:
            offset = linked['primer']['offset']
            for i in range(0, len(linked['end_primers'])):
                linked['end_primers'][i] = dict(linked['end_primers'][i])
                primer = linked['end_primers'][i]
                primer['seq'] = self.complement_sequence(primer['seq'])
                primer['pcr'] = sequence[
                    offset:primer['offset'] + len(primer['seq'])]
                del primer['offset']
            del linked['primer']['offset']