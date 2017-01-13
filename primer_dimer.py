COMPLEMENT_DICT = dict(A='T', T='A', C='G', G='C')


def check_bonds(primer_a, primer_b, required_bonds):
    bonds = 0
    for i in range(len(primer_a)):
        if COMPLEMENT_DICT[primer_a[i]] == primer_b[i]:
            bonds += 1
        if bonds == required_bonds:
            return True
    return False


def is_dimer(primer_a, primer_b, required_bonds=3):
    # Assume primers dont have whitespace and are uppercase
    large_primer = primer_a if len(primer_a) >= len(primer_b) else primer_b
    small_primer = primer_b if large_primer == primer_a else primer_a
    # Move the smallest primer along the larger primer
    start_index = len(small_primer) - required_bonds
    end_index = start_index + len(large_primer)
    moving_primer = small_primer + (" " * (len(large_primer) - required_bonds))
    for _ in range(len(moving_primer) - required_bonds):
        if check_bonds(large_primer, moving_primer[start_index:end_index],
                       required_bonds):
            return True
        moving_primer = " " + moving_primer[:-1]
    return False


def is_self_dimer(primer, required_bonds=3):
    return is_dimer(primer, primer, required_bonds)


def is_hairpin(primer, required_bonds=3):
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
    print(is_hairpin("ATCGGTTGGCCAATGC"))
    print(is_self_dimer("CGGCCG"))
