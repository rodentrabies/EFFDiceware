#! /usr/bin/python

# ------------------------------------------------------------------------------
# permute pages in PDF file to produce printable booklet layout
#
# TODO: add multiple levels for booklet (4, 8 pages per side)
#       currently only 2 pages per side are supported
# ------------------------------------------------------------------------------
import argparse

from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.pdf import PageObject


def booklet_pad(lst, empty):
    """
    Add elements to list `lst` to make it
    suitable for booklet permutation.
    """
    # add empty `page` and pad to even size
    return lst + [empty] * (4 - len(lst) % 4)


def booklet_permute(lst):
    """
    Create booklet permutation of list `lst`.
    Assume `lst` is padded properly.
    """
    n = len(lst)
    perm = []
    for i in range(n // 2):
        first, second = lst[i], lst[n - 1 - i]
        if i % 2 == 0:
            perm.append(second)
            perm.append(first)
        else:
            perm.append(first)
            perm.append(second)
    return perm


def booklet(lst, empty):
    "Generic booklet permutation operation."
    return booklet_permute(booklet_pad(lst, empty))


def transform_pdf(infile, outfile):
    """
    Read PDF file, extract list of pages, create empty PDF page
    and feed it to permutation operation, than print it into file.
    """
    inp = open(infile, 'rb')
    reader = PdfFileReader(inp)
    pages = [reader.getPage(i) for i in range(reader.getNumPages())]
    writer = PdfFileWriter()
    for p in booklet(pages, PageObject.createBlankPage(reader)):
        writer.addPage(p)
    with open(outfile, 'wb') as outp:
        writer.write(outp)
    inp.close()


def main():
    parser = argparse.ArgumentParser(
        description="Rearrange pages in PDF document for booklet printing."
    )
    parser.add_argument(
        'in',
        metavar='INPUT',
        help='file to transform'
    )
    parser.add_argument(
        'out',
        metavar='OUTPUT',
        help='file to output result of transformation'
    )
    args = vars(parser.parse_args())
    inp, outp = args['in'], args['out']
    # this check is necessary because of a bug in PyPDF2 library, which
    # leads to lost data when file read into PdfFileReader was overwritten
    if not inp == outp:
        transform_pdf(args['in'], args['out'])
    else:
        raise Exception('output file should be different from input')


if __name__ == "__main__":
    main()
