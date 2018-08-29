import os
import tempfile
import subprocess

import xml.etree.ElementTree as ET

from ddd.dependency import Dependency


EFFECTIVE_POM_CMD = 'mvn help:effective-pom -Doutput=%s'


def get_effective_pom(pom):
    """
    mvn help:effective-pom -Doutput=effective-pom.xml

    :param pom: The original pom file path
    :return: The effective pom XML
    """
    pom_path = os.path.dirname(pom)
    effective_pom_path = tempfile.NamedTemporaryFile(prefix='dirty-dependency-check',
                                                     suffix='xml',
                                                     delete=False).name

    cmd = EFFECTIVE_POM_CMD % effective_pom_path

    subprocess.check_output(cmd, shell=True, cwd=pom_path)

    if not os.path.exists(effective_pom_path):
        raise Exception('"%s" did not generate XML file.' % cmd)

    if not os.stat(effective_pom_path).st_size:
        raise Exception('"%s" generated empty XML file.' % cmd)

    result = file(effective_pom_path).read()
    os.remove(effective_pom_path)

    return result


def get_dependencies(effective_pom):
    """
    Parse the XML document passed as parameter and return a list of
    Dependency instances.

    Just interested in these XML nodes:

        <dependency>
          <groupId>org.apache.commons</groupId>
          <artifactId>commons-lang3</artifactId>
          <version>3.4</version>
        </dependency>

    :param effective_pom: XML document with effective POM
    :return: List with Dependency instances
    """
    dependencies = []

    namespaces = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}
    root = ET.fromstring(effective_pom)

    for dependency in root.findall('.//xmlns:dependency', namespaces=namespaces):
        artifact_id = dependency.find('xmlns:artifactId', namespaces=namespaces).text
        version = dependency.find('xmlns:version', namespaces=namespaces).text
        dependencies.append(Dependency(artifact_id, version))

    return dependencies
