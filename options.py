from optparse import OptionParser, Option, OptionValueError
from copy import copy

import os

__all__ = ['get_options']

_allowed_format_types = set(['db', 'xml', 'html', 'txt'])

def _check_format(option, opt, value):
    result = set(value.split('+'))

    if not result.issubset(_allowed_format_types):
        raise OptionValueError(
            "option %s: invalid value: %s" % (opt, '+'.join(result - _allowed_format_types)))
    return result

class SkHOption (Option):
    TYPES = Option.TYPES + ("format",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["format"] = _check_format


def get_options(version):
    parser = OptionParser(option_class=SkHOption, version="%%prog %s" % version)
    parser.add_option('-i', '--input-file', dest="filename", action="append", help="Input file (multiple)", metavar="FILE")
    parser.add_option('-l', '--list-file', dest="listfile", help="File with list of input files (one by line)", metavar="LIST")
    parser.add_option('-o', '--output-file', dest="destination", action="store", help="Output file name", metavar="DEST", default="export")
    parser.add_option('-t', '--type', dest="type", action="store", type="format", help="Type of export [xml|txt|html|db]", metavar="TYPE", default="db")

    (options, args) = parser.parse_args()

    if options.filename is None:
        options.filename = list()

    if args:
        options.filename.extend(args)

    try:
        if options.listfile:
            if not os.path.exists(options.listfile):
                raise OptionValueError("option %s: file %s not exist" % ('--list-file', options.listfile))

            options.filename.extend(
                [line.rstrip(' \n\r') for line in open(options.listfile)]
            )

        for f in options.filename:
            if not os.path.exists(f):
                raise OptionValueError("Data file %s not exist" % f)

    except OptionValueError as e:
        parser.error(e.msg)

    options.filename = list(set(options.filename))

    if not len(options.filename):
        parser.error('Empty input file set')

    out_dir = os.path.dirname(options.destination)
    out_file, format = os.path.splitext(os.path.basename(options.destination))
    format = format.lstrip('.')

    if out_dir == '':
        out_dir = os.getcwd()

    options.destination = os.path.join(out_dir, out_file)

    if format != '':
        options.type = _check_format(None, 'format', format)

    return options