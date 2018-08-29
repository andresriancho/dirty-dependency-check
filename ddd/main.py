import os
import json

from maven import get_effective_pom, get_dependencies
from nist import get_vulnerabilities_for


def main(pom, output):
    """

    :return: Process return code:
                0 for success
                1 for error
    """
    pom = os.path.expanduser(pom)
    output = os.path.expanduser(output)

    if not os.path.exists(pom):
        print('The pom file does not exist')
        return 1

    output_dir = os.path.dirname(output)
    if output_dir and not os.path.exists(output_dir):
        print('The directory "%s" does not exist' % output_dir)
        return 2

    try:
        output_fh = file(output, 'wb')
    except Exception, e:
        print('Failed to open file %s: "%s"' % (output, e))
        return 3

    try:
        effective_pom = get_effective_pom(pom)
        dependencies = get_dependencies(effective_pom)

        vulnerabilities = get_vulnerabilities_for(dependencies)
    except Exception, e:
        print(e)
        return 4

    vulnerabilities = make_serializable(vulnerabilities)
    json.dump(vulnerabilities, output_fh, indent=4)

    return 0


def make_serializable(vulnerabilities):
    result = []

    for vuln in vulnerabilities:
        serializable = {'dependency_name': vuln.dependency_name,
                        'dependency_version': vuln.dependency_version,
                        'cve': vuln.cve,
                        'cvss': vuln.cvss,
                        'nist': {'product_name': vuln.nist_product_name,
                                 'vendor_name': vuln.nist_vendor_name}}

        result.append(serializable)

    return result
