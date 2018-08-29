#!/usr/bin/env python

import sys
import argparse

from ddd.main import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dirty dependency check')
    parser.add_argument('--pom', required=True, help='Path to pom.xml file')
    parser.add_argument('--output', required=True, help='Output JSON file')

    args = parser.parse_args()

    sys.exit(main(args.pom, args.output))
