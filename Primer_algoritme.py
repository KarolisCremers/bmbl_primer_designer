"""
This programme gives all the available primers of the given length
in the given primer-region. If there are no primers found,
then a primer there will a primer will be sought with additional
length.
The information about the found primers is given in a
specific order:
primer sequence,
primer length,
CG percentage,
melting temperature and
location counted from the ends of the input sequence.

IMPORTANT:
Only primers with the right CG percentage and melting temperature
are given back. THIS CODE DOES NOT CHECK FOR HAIPIN LOOPS AND PRIMER-DIMERS.

Author: Karolis Cremers, Wesley Ameling
"""
from re import match, IGNORECASE


## ==============================================================
## = LET OP: Ik ben overgegaan naar een object geörienteerde    =
## = structuur, zie het bestand TargetPrimerFinder waar jouw    =
## = algoritme geïmplementeerd kan worden.                      =
## ==============================================================

def calc_primer_details(primer):
    """ Calculates the melting temperature and GC% of a primer which
    has a length less than 25 nucleotides.
    """
    ## DEZE FUNCTIE IS NIET MEER NODIG IN HET OBJECT GEORIENTEERDE
    if not match('^[ATCG]+$', primer, IGNORECASE):
        raise Exception('Primer contains non-base characters!')
    gc_length = 0
    for base in primer:
        if match('[GC]', base, IGNORECASE):
            gc_length += 1
    # Calculate the GC%
    gc_perc = (float(gc_length) / len(primer)) * 100
    # Calculate the melting temp
    melting_temp = 4 * gc_length + 2 * (len(primer) - gc_length)
    return gc_perc, melting_temp

## ==============================================================
## = LET OP: Ik ben overgegaan naar een object geörienteerde    =
## = structuur, zie het bestand TargetPrimerFinder waar jouw    =
## = algoritme geïmplementeerd kan worden.                      =
## ==============================================================

def primer_finder(primer_region, primer_length):
    """
    This function send the appropriate sequence to the function
    calc_primer_details.
    The results from this function and other necessary information
    such as primer length, position, and sequence is given for
    each found primer.
    If no primer is found by the given length then one nucleotide
    is added to allowed primer length. This continuous until
    the maximum primer length of 30 is reached or a primer is found.
    """
    primers = []
    while primers == [] or 30 <= primer_length:
        for position in range(0, len(primer_region)):
            primer = []
            gc_perc, melting_temp = calc_primer_details(primer_region[position:(position + int(primer_length))])
            primer.append(primer_region[position:(position + int(primer_length))])
            primer.append(primer_length)
            primer.append(gc_perc)
            primer.append(melting_temp)
            primer.append(position)
            if 50 <= gc_perc <= 60:
                if 55 <= melting_temp <= 65:
                    primers.append(primer)
        if not primers:
            primer_length += 1
    return primers

## ==============================================================
## = LET OP: Ik ben overgegaan naar een object geörienteerde    =
## = structuur, zie het bestand TargetPrimerFinder waar jouw    =
## = algoritme geïmplementeerd kan worden.                      =
## ==============================================================

def reverse_flipper(reverse_primer_region, primer_length):
    """
    This function converts the given reverse primer region
    to the right right binding strand.
    """
    ## DEZE FUNCTIE IS NIET MEER NODIG IN HET OBJECT GEORIENTEERDE
    reverse_primer_region_flipped = ""
    for nucleotide in range((len(reverse_primer_region) - 1), 0, -1):
        #volgens mij raak ik hier een nucleotide kwijt maar zonder de - 1 wilt hij het niet doen.
        if reverse_primer_region[nucleotide] == "A" or reverse_primer_region[nucleotide] == "a":
            reverse_primer_region_flipped += "t"
        if reverse_primer_region[nucleotide] == "T" or reverse_primer_region[nucleotide] == "t":
            reverse_primer_region_flipped += "a"
        if reverse_primer_region[nucleotide] == "C" or reverse_primer_region[nucleotide] == "c":
            reverse_primer_region_flipped += "g"
        if reverse_primer_region[nucleotide] == "G" or reverse_primer_region[nucleotide] == "g":
            reverse_primer_region_flipped += "c"
    reverse_primers = primer_finder(reverse_primer_region_flipped, primer_length)
    return reverse_primers

## ==============================================================
## = LET OP: Ik ben overgegaan naar een object geörienteerde    =
## = structuur, zie het bestand TargetPrimerFinder waar jouw    =
## = algoritme geïmplementeerd kan worden.                      =
## ==============================================================

def sequence_cutter(sequence_input, starget_start, target_end, primer_length):
    """
    This function extracts the regions wherein
    the primers will be searched.
    These regions are put in the variables:
    forward_primer_region and reverse_primer_region.
    """
    forward_primer_region = sequence_input[:(starget_start + primer_length)]
    reverse_primer_region = sequence_input[((target_end - primer_length) - 1):]
    return forward_primer_region, reverse_primer_region

## ==============================================================
## = LET OP: Ik ben overgegaan naar een object geörienteerde    =
## = structuur, zie het bestand TargetPrimerFinder waar jouw    =
## = algoritme geïmplementeerd kan worden.                      =
## ==============================================================

def main():
    """
    This function gives the inputs of the user to
    the appropriate functions.
    """
    sequence_input = "tcaggc tcggtggttc tcgtgtaccc" \
                      "ctacagcgag aaatcggata aactattaca acccctacag tttgatgagt atagaaatgg" \
                      "atccactcgt tattctcgga cgagtgttca gtaatgaacc tctggagaga accatgtata" \
                      "tgatcgttat ctgggttgga cttctgcttt taagcccaga taactggcct gaatatgtta" \
                      "atgagagaat cggtattcct catgtgtggc atgttttcgt ctttgctctt gcattttcgc" \
                      "tagcaattaa tgtgcatcga ttatcagcta ttgccagcgc cagatataag cgatttaagc" \
                      "taagaaaacg cattaagatg caaaacgata aagtgcgatc agtaattcaa aaccttacag" \
                      "aagagcaatc tatggttttg tgcgcagccc ttaatgaagg caggaagtat gtggttacat" \
                      "caaaacaatt cccatacatt agtgagttga ttgagcttgg tgtgttgaac aaaacttttt" \
                      "cccgatggaa tggaaagcat atattattcc ctattgagga tatttactgg actgaattag" \
                      "ttgccagcta tgatccatat aatattgaga taaagccaag gccaatatct aagtaactag" \
                      "ataagaggaa tcgattttcc cttaattttc tggcgtccac tgcatgttat gccgcgttcg" \
                      "ccaggcttgc tgtaccatgt gc"
    primer_length = int("17")
    target_start = int('30')
    target_end = int('600')
    sequence_input = sequence_input.replace(" ", "")
    forward_primer_region, reverse_primer_region = sequence_cutter(
        sequence_input, target_start, target_end, primer_length)
    forward_primers = primer_finder(forward_primer_region, primer_length)
    print("forward primers calculated!")
    reverse_primers = reverse_flipper(reverse_primer_region, primer_length)
    print("reverse primers caclulated!")
    print("forward:")
    print(forward_primers)
    print("reverse:")
    print(reverse_primers)

## ==============================================================
## = LET OP: Ik ben overgegaan naar een object geörienteerde    =
## = structuur, zie het bestand TargetPrimerFinder waar jouw    =
## = algoritme geïmplementeerd kan worden.                      =
## ==============================================================

main()
