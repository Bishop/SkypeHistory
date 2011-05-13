import sys
from optparse import OptionParser

VERSION = "0.0.1"

parser = OptionParser(version="%%prog %s" % VERSION)
parser.add_option('-i', '--input-file', dest="filename", action="append", help="Input file (multiple)", metavar="FILE")
parser.add_option('-o', '--output-file', dest="destination", action="store", help="Output file name", metavar="DEST")
parser.add_option('-t', '--type', dest="type", action="store", help="Type of export [xml|txt|html|db]", metavar="TYPE", default="db")


(options, args) = parser.parse_args()

print options
print args