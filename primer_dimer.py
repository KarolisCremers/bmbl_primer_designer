COMPLEMENT_DICT = dict(A='T', T='A', C='G', G='c')


def check_bonds(primer_a, primer_b, required_bonds):
    bonds = 0
    for i in range(len(primer_a)):
        if COMPLEMENT_DICT[primer_a[i]] == primer_b[i]:
            bonds += 1
        if bonds == required_bonds:
            return True


def primer_space_generator(primer, length):
    required_spaces = length - len(primer)
    for i in range(required_spaces + 1):
        pre_spaces = i * " "
        post_spaces = (required_spaces - i) * " "
        yield pre_spaces + primer + post_spaces


def is_dimer(primer_a, primer_b, required_bonds=3):
    # Assume primers dont have whitespace and are uppercase
    large_primer = primer_a if len(primer_a) >= len(primer_b) else primer_b
    small_primer = primer_b if large_primer == primer_a else primer_a
    for primer in primer_space_generator(small_primer, len(large_primer)):
        if check_bonds(large_primer, primer, required_bonds):
            return True
    return False


def is_self_dimer(primer, required_bonds=3):
    if len(primer) < required_bonds * 2:
        return False
    for i in range(required_bonds + 1, len(primer)):
        primer_a = primer[:i - 1]
        primer_b = primer[i + 1:]
        len_difference = abs(len(primer_a) - len(primer_b))
        full_primer = primer_a if len(primer_a) > len(primer_b) else primer_b
        padded_primer = (" " * len_difference) + (
            primer_b if full_primer == primer_a else primer_a)
        if is_dimer(full_primer, padded_primer, required_bonds):
            return True
    return False

if __name__ == '__main__':
    print(is_dimer("ATCGGTTGGCCAATGC", "AATGGCCTGA"))
    print(is_self_dimer("ATCGGTTGGCCAATGC"))
