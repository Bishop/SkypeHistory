from optparse import OptionParser, Option, OptionValueError
from copy import copy

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
    parser.add_option('-o', '--output-file', dest="destination", action="store", help="Output file name", metavar="DEST")
    parser.add_option('-t', '--type', dest="type", action="store", type="format", help="Type of export [xml|txt|html|db]", metavar="TYPE", default="db")

    return parser.parse_args()