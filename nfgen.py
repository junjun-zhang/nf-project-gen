#!/usr/bin/env python3

import os
import argparse
from cookiecutter.main import cookiecutter

GEN_HOME = os.path.dirname(os.path.realpath(__file__))


def main(gen_type):
    project_dir = ''
    module_dir = ''
    cwd = os.getcwd()

    if gen_type in ('p', 'pm'):
        print('*** Gather information to generate Nextflow project template ***')
        project_dir = cookiecutter('%s/project-template/' % GEN_HOME)

    if project_dir:
        print('Nextflow project template generated in: %s\n' % project_dir)

    if gen_type in ('pm', 'm'):
        if project_dir:
            os.chdir(os.path.join(project_dir, 'tools'))

        print('*** Gather information to generate Nextflow module template ***')
        module_dir = cookiecutter('%s/module-template/' % GEN_HOME)

        os.chdir(cwd)

    if module_dir:
        print('Nextflow module template generated in: %s' % module_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Nextflow template generation')
    parser.add_argument('-g', '--gen-type', dest='gen_type', type=str,
                        choices=['p', 'pm', 'm'], required=True,
                        help='Specify type of template to generate, available options: '
                             'p - project; pm - project and module; m - module')
    args = parser.parse_args()

    main(args.gen_type)
