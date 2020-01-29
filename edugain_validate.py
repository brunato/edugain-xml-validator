#!/usr/bin/env python3
#
# Copyright (c) 2019, SISSA (Scuola Internazionale Superiore di Studi Avanzati).
# All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#


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
    parser.add_argument(
        '--cert', default=None, metavar="CERT_FILE",
        help="Validate eduGAIN XML data files using provided certificate."
    )
    parser.add_argument(
        '--lazy', action='store_true', default=False,
        help="Use xmlschema lazy validation mode (slower but use less memory). "
             "Not used when XML signature validation is requested."
    )

    parser.add_argument(dest='xml_file', metavar='XML_FILE', nargs='+',
                        help="XML filename.")
    return parser.parse_args()


if __name__ == '__main__':
    import os
    import logging
    import sys
    import datetime
    import lxml.etree
    import signxml
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
        'http://www.w3.org/XML/1998/namespace':
            'xml.xsd',
        'urn:oasis:names:tc:SAML:metadata:rpi':
            'saml-metadata-rpi-v1.0-csd01.xsd',
        'urn:oasis:names:tc:SAML:profiles:SSO:idp-discovery-protocol':
            'sstc-saml-idp-discovery.xsd',
        'urn:oasis:names:tc:SAML:metadata:algsupport':
            'sstc-saml-metadata-algsupport-cd01.xsd',
        'http://www.w3.org/2005/08/addressing':
            'ws-addr.xsd',
        'http://docs.oasis-open.org/ws-sx/ws-securitypolicy/200702':
            'ws-securitypolicy-1.2.xsd',
        'http://docs.oasis-open.org/wsfed/authorization/200706':
            'ws-authorization.xsd',
        'http://docs.oasis-open.org/wsfed/federation/200706':
            'ws-federation.xsd',
        'http://schemas.xmlsoap.org/ws/2004/09/mex':
            'MetadataExchange.xsd',
        'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd':
            'oasis-200401-wss-wssecurity-utility-1.0.xsd',
        'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd':
            'oasis-200401-wss-wssecurity-secext-1.0.xsd',
        'urn:oasis:names:tc:SAML:metadata:attribute':
            'sstc-metadata-attr.xsd',
        'urn:oasis:names:tc:SAML:metadata:ui':
            'sstc-saml-metadata-ui-v1.0.xsd',
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

    print("*** eduGAIN XML metadata validation script ***\n")

    if args.cert is None:
        cert = None
    else:
        with open(args.cert) as fh:
            cert = fh.read()
        print("Use certificate file {!r} for signature validation ...".format(args.cert))
        if args.verbosity >= 2:
            print("Verify XML signatures with certificate:\n")
            print(cert)

    locations = LOCATIONS.copy()
    if args.skip_optional:
        print("Building schema instance with minimal metadata (no 'lax' wildcards validation) ...")
    else:
        locations.update(OPTIONAL_LOCATIONS)
        print("Building schema instance with full eduGAIN metadata ...")

    schemas_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'schemas/')
    xsd_file = os.path.join(schemas_dir, 'shibboleth-metadata-1.0.xsd')

    start_dt = datetime.datetime.now()
    schema = xmlschema.XMLSchema(xsd_file, locations=locations, loglevel=loglevel)
    elapsed_time = datetime.datetime.now() - start_dt
    print("Schema: OK (elapsed time: {})".format(elapsed_time))

    exit_code = 0
    for xml_file in args.xml_file:
        print("\nValidate XML file {!r} ...".format(xml_file))
        start_dt = datetime.datetime.now()

        try:
            if cert is not None:
                signed_xml_data = lxml.etree.parse(xml_file).getroot()
                signxml.XMLVerifier().verify(signed_xml_data, x509_cert=cert)

                elapsed_time = datetime.datetime.now() - start_dt
                print("XML signature validation: OK (elapsed time: {})".format(elapsed_time))
                start_dt = datetime.datetime.now()
                xml_file = signed_xml_data

            xmlschema.validate(xml_file, schema=schema, lazy=args.lazy)

        except xmlschema.XMLSchemaValidationError as err:
            exit_code = 1
            print("XML schema validation: FAIL")
            if args.verbosity >= 2:
                print(err)

        except (signxml.InvalidDigest, signxml.InvalidSignature) as err:
            exit_code = 1
            print("XML signature validation: FAIL")
            if args.verbosity >= 2:
                print(err)
        else:
            elapsed_time = datetime.datetime.now() - start_dt
            print("XML schema validation: OK (elapsed time: {})".format(elapsed_time))

    exit(code=exit_code)
