from optparse import OptionParser

class Init():
    def parse_options():
        parser = OptionParser()
        parser.add_option('-r', '--revert', action='store_true', default=False, dest='revert', help="Path to access logs")
        options, args = parser.parse_args()
        return options, args