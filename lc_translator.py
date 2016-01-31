def build_lc_translator(string):
    '''
    Generative function that returns a translator from (lineno, col_offset)
    pairs to absolute position in the string.
    '''
    line_lengths = [len(line) for line in string.split('\n')]
    accumulated_line_lengths = [0]
    for ll in line_lengths:
        accumulated_line_lengths.append(accumulated_line_lengths[-1] + ll + 1)

    def translator(lineno, col_offset):
        return accumulated_line_lengths[lineno - 1] + col_offset

    return translator


