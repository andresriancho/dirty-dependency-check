import os
import gzip
import json

from ddd.vulnerability import Vulnerability


DATA_PATH = os.path.realpath(os.path.join(__file__, '..', '..', 'data'))


def get_vulnerabilities_for(dependencies):
    """
    Search the NIST DB for vulnerabilities in the identified dependencies

    :param dependencies: A list of Dependency instances
    :return: A list of vulnerabilities
    """
    vulnerabilities = []

    for db in get_all_databases(DATA_PATH):
        for vuln in db.search(dependencies):
            vulnerabilities.append(vuln)

    return vulnerabilities


def get_all_databases(data_path):
    for compressed_db_path in os.listdir(data_path):
        db_fh = gzip.open(os.path.join(data_path, compressed_db_path))
        db = DataBase(db_fh)
        yield db


class DataBase(object):
    def __init__(self, db_fh):
        self.db = json.load(db_fh)

    def search(self, dependencies):
        for cve_item in self.db['CVE_Items']:

            for affected_vendor in self.get_affected_vendors(cve_item):
                for dependency in dependencies:
                    if self.dependency_matches_affected_vendor(dependency, affected_vendor):
                        yield Vulnerability.from_parts(dependency,
                                                       affected_vendor,
                                                       cve_item)

    def get_affected_vendors(self, cve_item):
        try:
            for vendor_data in cve_item['cve']['affects']['vendor']['vendor_data']:
                for product_data in vendor_data['product']['product_data']:

                    yield Affected(vendor_data['vendor_name'],
                                   product_data['product_name'],
                                   product_data['version']['version_data'])
        except KeyError, e:
            data = json.dumps(cve_item, indent=4)
            raise Exception('Unexpected NIST DB format. KeyError %s\n\n%s' % (e, data))

    def dependency_matches_affected_vendor(self, dependency, affected_vendor):
        if dependency.name not in (affected_vendor.product_name, affected_vendor.vendor_name):
            return False

        if not self.matches_version(dependency, affected_vendor):
            return False

        return True

    def matches_version(self, dependency, affected_vendor):
        for version in affected_vendor.version_data:
            if version['version_value'] == dependency.version:
                return True

        return False


class Affected(object):
    __slots__ = ('vendor_name', 'product_name', 'version_data')

    def __init__(self, vendor_name, product_name, version_data):
        """
        :param vendor_name: The vendor name 'pivotal'
        :param product_name: The product name 'springframework'
        :param version: The affected version
        """
        self.vendor_name = vendor_name.lower()
        self.product_name = product_name.lower()
        self.version_data = version_data
