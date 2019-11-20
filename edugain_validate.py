#!/usr/bin/env python


def parse_args():
    """Command arguments parsing"""
    import argparse

    parser = argparse.ArgumentParser(description="This program validates eduGAIN XML data files")
    parser.add_argument(
        '-v', dest='verbosity', action='count', default=0, help="Increase output verbosity."
    )
    parser.add_argument(
        '-s', dest='skip_optional', action='store_true', default=False,
        help="Skip optional schemas related to XSD wildcards."
    )
    parser.add_argument(dest='xml_file', metavar='XML_FILE', help="XML input filename.")
    return parser.parse_args()


if __name__ == '__main__':
    import os
    import logging
    import sys
    import xmlschema


    # These are the explicit minimal namespaces required to validate eduGAIN XML,
    # followed by a list of optional namespaces for full XML data validation
    # comprehensive of xs:any 'lax' wildcards.
    #
    # Ref: https://wiki.geant.org/display/eduGAIN/Metadata+Aggregation+Practice+Statement

    LOCATIONS = {
        # 'urn:mace:shibboleth:metadata:1.0': 'shibboleth-metadata-1.0.xsd',
        'urn:oasis:names:tc:SAML:2.0:metadata': 'saml-schema-metadata-2.0.xsd',
        'urn:oasis:names:tc:SAML:2.0:protocol': 'saml-schema-protocol-2.0.xsd',
        'urn:oasis:names:tc:SAML:2.0:assertion': 'saml-schema-assertion-2.0.xsd',
        'http://www.w3.org/2000/09/xmldsig#': 'xmldsig-core-schema.xsd',
        'http://www.w3.org/2001/04/xmlenc#': 'xenc-schema.xsd',
    }

    OPTIONAL_LOCATIONS = {
        'http://www.w3.org/XML/1998/namespace': 'xml.xsd',
        'urn:oasis:names:tc:SAML:metadata:rpi': 'saml-metadata-rpi-v1.0-csd01.xsd',
        'urn:oasis:names:tc:SAML:profiles:SSO:idp-discovery-protocol': 'sstc-saml-idp-discovery.xsd',
        'urn:oasis:names:tc:SAML:metadata:algsupport': 'sstc-saml-metadata-algsupport-cd01.xsd',
        'http://www.w3.org/2005/08/addressing': 'ws-addr.xsd',
        'http://docs.oasis-open.org/ws-sx/ws-securitypolicy/200702': 'ws-securitypolicy-1.2.xsd',
        'http://docs.oasis-open.org/wsfed/authorization/200706': 'ws-authorization.xsd',
        'http://docs.oasis-open.org/wsfed/federation/200706': 'ws-federation.xsd',
        'http://schemas.xmlsoap.org/ws/2004/09/mex': 'MetadataExchange.xsd',
        'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd':
            'oasis-200401-wss-wssecurity-utility-1.0.xsd',
        'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd':
            'oasis-200401-wss-wssecurity-secext-1.0.xsd',
        'urn:oasis:names:tc:SAML:metadata:attribute': 'sstc-metadata-attr.xsd',
        'urn:oasis:names:tc:SAML:metadata:ui': 'sstc-saml-metadata-ui-v1.0.xsd',
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


    locations = LOCATIONS.copy()
    if args.skip_optional:
        print("Building schema instance with minimal metadata (no 'lax' wildcards validation) ...\n")
    else:
        locations.update(OPTIONAL_LOCATIONS)
        print("Building schema instance with full eduGAIN metadata ...\n")

    schemas_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'schemas/')
    xsd_file = os.path.join(schemas_dir, 'shibboleth-metadata-1.0.xsd')
    schema = xmlschema.XMLSchema(xsd_file, locations=locations, loglevel=loglevel)

    print("Validate XML file {!r} ...\n".format(args.xml_file))
    xmlschema.validate(args.xml_file, schema=schema)
    print("Validation: OK")