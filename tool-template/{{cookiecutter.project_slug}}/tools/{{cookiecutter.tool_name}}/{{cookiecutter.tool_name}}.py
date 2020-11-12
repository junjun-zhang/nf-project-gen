#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse


def main():
    """
    Python implementation of tool: {{ cookiecutter.tool_name }}

    This is auto-generated Python code, please update as needed!
    """

    parser = argparse.ArgumentParser(description='Tool: {{ cookiecutter.tool_name }}')
    parser.add_argument('-i', '--input-file', dest='input_file', type=str,
                        help='Input file', required=True)
    parser.add_argument('-o', '--output-dir', dest='output_dir', type=str,
                        help='Output directory', required=True)
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        sys.exit('Error: specified input file %s does not exist or is not accessible!' % args.input_file)

    if not os.path.isdir(args.output_dir):
        sys.exit('Error: specified output dir %s does not exist or is not accessible!' % args.output_dir)

    with open(os.path.join(args.output_dir, 'input_file_name.txt'), 'w') as f:
        f.write("The input file name is %s\n" % args.input_file)


if __name__ == "__main__":
    main()
