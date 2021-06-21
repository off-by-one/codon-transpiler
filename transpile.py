#!/usr/bin/python3
import itertools

dna = {'A', 'T', 'G', 'C'}

def is_base(b):
    return b in dna

def is_codon(c):
    return len(c) == 3 and all(is_base(b) for b in c)

def read_dna(filename):
    file_contents = ''
    with open(filename) as dna_file:
        file_contents = dna_file.read()
    return filter(is_base, file_contents)

def read_table(filename):
    import csv
    with open(filename, newline='') as csvfile:
        table = {}
        table_reader = csv.reader(csvfile, delimiter=',')
        next(table_reader) # skip first row, assume it is row labels
        for row in table_reader:
            if not is_codon(row[-1]) or not is_codon(row[0]):
                continue
            table[row[0]] = row[-1]
        return table


def dna_to_rna(sequence):
    return map(lambda b : b if b != 'T' else 'U', sequence)

def rna_to_dna(sequence):
    return map(lambda b : b if b != 'U' else 'T', sequence)

def seq_to_codon(sequence):
    codon = ''
    for b in sequence:
        if len(codon) < 3:
            codon += b
        if len(codon) == 3:
            yield codon
            codon = ''
    assert codon == '', "sequence must be divisible into sets of three codons"

def codon_to_seq(codons):
    return itertools.chain.from_iterable(codons)


def transpile(table, codons):
    for c in codons:
        if c in table:
            yield table[c]
        else:
            yield c


def main():
    from optparse import OptionParser
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) != 2:
        print("Usage is: python3 transpile.py <table filename> <sequence filename>")

    table_file, sequence_file = args
    table = read_table(table_file)
    sequence = read_dna(sequence_file)

    codons = seq_to_codon(sequence)
    new_codons = transpile(table, codons)
    new_sequence = codon_to_seq(new_codons)

    for b in new_sequence:
        print(b, end='')


def tests():
    assert list(dna_to_rna('ATGC')) == list('AUGC')
    assert list(rna_to_dna('AUGC')) == list('ATGC')
    assert list(seq_to_codon('AUGUCA')) == ['AUG', 'UCA']
    assert list(codon_to_seq(['AUG', 'UCA'])) == list('AUGUCA')

if __name__ == '__main__':
    main()
