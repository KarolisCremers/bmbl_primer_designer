import re
from primer_dimer import is_dimer, is_self_dimer


def calc_primer_details(primer):
    ''' Calculates the melting temperature and GC% of a primer which
    has a length less than 25 nucleotides.
    '''
    if not re.match('^[ATCG]+$', primer):
        raise Exception('Primer contains non-base characters!')
    gc_length = len(re.findall('[GC]', primer))
    # Calculate the GC%
    gc_perc = (float(gc_length) / len(primer)) * 100
    # Calculate the melting temp
    melting_temp = 4 * gc_length + 2 * (len(primer) - gc_length)
    return gc_perc, melting_temp


def find_all_primers(primer_region):
    offset = 0
    primer_tracker = set()
    found_primers = []
    while len(primer_region) >= offset + 17:
        current_region = primer_region[offset:]
        for primer_length in range(17, min(26, len(primer_region) - offset)):
            primer = current_region[:primer_length]
            gc_perc, melting_temp = calc_primer_details(primer)
            if 50 <= gc_perc <= 60 and 55 <= melting_temp <= 65:
                # Duplicate primers are unuseable
                if primer in primer_tracker:
                    # filter out this primer because it can anneal on multiple
                    # sites
                    found_primers = list(
                        filter(lambda o: o["seq"] in primer_tracker,
                               found_primers))
                else:
                    primer_tracker.add(primer)
                    found_primers.append(dict(seq=primer, gc_perc=gc_perc,
                                              melt_temp=melting_temp,
                                              offset=offset))
        offset += 1
    # Future: filter out hairpins
    # Filter out self dimers
    return list(filter(lambda p: not is_self_dimer(p['seq']), found_primers))


def primer_filter(primer, max_pcr):
    ost = primer['offset']
    melt_temp = primer['melt_temp']
    return lambda o: (o['offset'] - ost + len(o['seq']) <= max_pcr and
                      ost + len(primer['seq']) <= o['offset'] and
                      abs(o['melt_temp'] - melt_temp) <= 5 and
                      not is_dimer(primer['seq'], o['seq']))


def link_primers(primer_list, max_pcr):
    links = []
    for _ in range(0, len(primer_list)):
        link = dict(primer=primer_list[0])
        del primer_list[0]
        link['end_primers'] = list(filter(primer_filter(link['primer'],
                                                        max_pcr),
                                          primer_list))
        # Only when primers are available, add it to the links
        if link['end_primers']:
            # Sort the list by length of the pcr product and then the
            # melting_temp
            link['end_primers'].sort(key=lambda o: o['offset'], reverse=True)
            link['end_primers'].sort(key=lambda o: abs(
                o['melt_temp'] - link['primer']['melt_temp']))
            links.append(link)
    return links


def nucleotide_complement(sequence):
    comp_dict = dict(A='T', T='A', C='G', G='C')
    complement = ''
    for nucleotide in sequence[::-1]:
        complement += comp_dict[nucleotide]
    return complement


def find_primers(sequence, range_minimum, range_maximum, pcr_max):
    sequence = ''.join(re.split('\s+', sequence)).upper()
    range_minimum -= 1
    range_maximum -= 1
    sequence = sequence[range_minimum:range_maximum]
    linked_primers = link_primers(find_all_primers(sequence), pcr_max)
    # Make sure the reversed primers are actually reversed
    # Also get the product size
    for linked in linked_primers:
        offset = linked['primer']['offset']
        for i in range(0, len(linked['end_primers'])):
            linked['end_primers'][i] = dict(linked['end_primers'][i])
            primer = linked['end_primers'][i]
            primer['seq'] = nucleotide_complement(primer['seq'])
            primer['pcr'] = sequence[
                offset:primer['offset'] + len(primer['seq'])]
            del primer['offset']
        del linked['primer']['offset']
    return linked_primers


if __name__ == '__main__':
    sequence_input = 'tcaggc tcggtggttc tcgtgtaccc' \
        'ctacagcgag aaatcggata aactattaca acccctacag tttgatgagt atagaaatgg' \
        'atccactcgt tattctcgga cgagtgttca gtaatgaacc tctggagaga accatgtata' \
        'tgatcgttat ctgggttgga cttctgcttt taagcccaga taactggcct gaatatgtta' \
        'atgagagaat cggtattcct catgtgtggc atgttttcgt ctttgctctt gcattttcgc' \
        'tagcaattaa tgtgcatcga ttatcagcta ttgccagcgc cagatataag cgatttaagc' \
        'taagaaaacg cattaagatg caaaacgata aagtgcgatc agtaattcaa aaccttacag' \
        'aagagcaatc tatggttttg tgcgcagccc ttaatgaagg caggaagtat gtggttacat' \
        'caaaacaatt cccatacatt agtgagttga ttgagcttgg tgtgttgaac aaaacttttt' \
        'cccgatggaa tggaaagcat atattattcc ctattgagga tatttactgg actgaattag' \
        'ttgccagcta tgatccatat aatattgaga taaagccaag gccaatatct aagtaactag' \
        'ataagaggaa tcgattttcc cttaattttc tggcgtccac tgcatgttat gccgcgttcg' \
        'ccaggcttgc tgtaccatgt gc'
    range_minimum = 1
    range_maximum = 707
    max_pcr = 200
    print(find_primers(sequence_input, range_minimum, range_maximum, max_pcr))
