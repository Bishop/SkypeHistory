import sys
import options

VERSION = "0.0.1"

(options, args) = options.get_options(VERSION)

print options
print args