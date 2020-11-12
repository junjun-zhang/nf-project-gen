#!/usr/bin/env python3

import os
import argparse
from cookiecutter.main import cookiecutter
from cookiecutter.config import get_user_config
from cookiecutter.replay import load

GEN_HOME = os.path.dirname(os.path.realpath(__file__))


def template_gen(template_name, config_dict):
    print('*** Gather information to generate Nextflow %s ***' % template_name.replace('-', ' '))
    project_dir = cookiecutter(os.path.join(GEN_HOME, template_name))

    project_context = load(config_dict['replay_dir'], template_name)
    print('Template generated in: %s\n' % project_dir)

    return project_dir, project_context


def main(gen_type, commit=False, config_file=None):
    project_dir = ''
    module_dir = ''
    cwd = os.getcwd()

    config_dict = get_user_config(config_file=config_file)

    if gen_type in ('p', 'pm'):
        project_dir, project_context = template_gen('project-template', config_dict)
        # print(project_context)

    if gen_type in ('pm', 'm'):
        if project_dir:
            os.chdir(os.path.join(project_dir, 'tools'))

        module_dir, module_context = template_gen('module-template', config_dict)
        # print(module_context)

        os.chdir(cwd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Nextflow template generation')
    parser.add_argument('-g', '--gen-type', dest='gen_type', type=str,
                        choices=['p', 'pm', 'm'], required=True,
                        help='Specify type of template to generate, available options: '
                             'p - project; pm - project and module; m - module')
    parser.add_argument('-a', '--auto-commit', dest='commit', action='store_true',
                        help='Perform git commit after template generated')
    parser.add_argument('-c', '--config-file', dest='config_file',
                        help='User configuration file path')
    args = parser.parse_args()

    main(
        gen_type=args.gen_type,
        commit=args.commit,
        config_file=args.config_file
    )
