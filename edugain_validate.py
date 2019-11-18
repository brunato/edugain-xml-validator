#!/usr/bin/env python


def parse_args():
    """Command arguments parsing"""
    import argparse

    parser = argparse.ArgumentParser(description="This program validates eduGAIN XML data files")
    parser.add_argument('-v', dest='verbosity', action='count', default=0, help="Increase output verbosity.")
    parser.add_argument(dest='xml_file', metavar='XML_FILE', help="XML input filename.")
    return parser.parse_args()


if __name__ == '__main__':
    import os
    import logging
    import sys
    import xmlschema

    LOCATIONS = {
        # 'urn:mace:shibboleth:metadata:1.0': 'shibboleth-metadata-1.0.xsd',
        'urn:oasis:names:tc:SAML:2.0:metadata': 'saml-schema-metadata-2.0.xsd',
        'urn:oasis:names:tc:SAML:2.0:protocol': 'saml-schema-protocol-2.0.xsd',
        'urn:oasis:names:tc:SAML:2.0:assertion': 'saml-schema-assertion-2.0.xsd',
        'http://www.w3.org/2000/09/xmldsig#': 'xmldsig-core-schema.xsd',
    }

    if sys.version_info < (3, 5, 0):
        sys.stderr.write("You need python 3.5 or later to run this program\n")
        sys.exit(1)

    args = parse_args()

    if args.verbosity <= 0:
        loglevel = logging.ERROR
    elif args.verbosity == 1:
        loglevel = logging.WARNING
    elif args.verbosity == 2:
        loglevel = logging.INFO
    else:
        loglevel = logging.DEBUG

    if args.verbosity:
        print("Building schema instance ...")

    schemas_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'schemas/')
    xsd_file = os.path.join(schemas_dir, 'shibboleth-metadata-1.0.xsd')
    schema = xmlschema.XMLSchema(xsd_file, locations=LOCATIONS, loglevel=loglevel)

    if args.verbosity:
        print("Validate eduGAIN XML file ...")

    xmlschema.validate(args.xml_file, schema=schema)
