#!/usr/bin/env python3

import os
import argparse
import subprocess
from cookiecutter.main import cookiecutter
from cookiecutter.config import get_user_config
from cookiecutter.replay import load

GEN_HOME = os.path.dirname(os.path.realpath(__file__))


def git_init_push(local_path, github_acc, repo, branch='main'):
    cmd = f"""
        cd {local_path} && \
        git init && \
        git add . && \
        git commit -m "initial commit with auto-generated Nextflow project template" && \
        git branch -M {branch} && \
        git remote add origin git@github.com:{github_acc}/{repo}.git && \
        git push -u origin {branch}
    """

    # print(cmd)
    print(f"Initialize git repo and push to remote at: https://github.com/{github_acc}/{repo}")
    subprocess.run(cmd, shell=True, check=True)


def git_commit_push(local_path, branch, message):
    cmd = f"""
        cd {local_path} && \
        git checkout -b {branch} && \
        git add . && \
        git commit -m "{message}" && \
        git push --set-upstream origin {branch}
    """

    # print(cmd)
    print(message)
    subprocess.run(cmd, shell=True, check=True)


def docker_build_push(build_path, quay_io_acc, repo, tag, push=False):
    cmd = f"""
        cd {build_path} \
        && docker build -t quay.io/{quay_io_acc}/{repo}:{tag} . \
    """
    print(f"Build docker image quay.io/{quay_io_acc}/{repo}:{tag}")

    if push:
        print(f"... and push to Quay: https://quay.io/repository/{quay_io_acc}/{repo}?tab=tags")
        cmd = f"{cmd} && docker push quay.io/{quay_io_acc}/{repo}:{tag}"

    # print(cmd)
    subprocess.run(cmd, shell=True, check=True)


def template_gen(template_name, config_file, no_input, extra_context={}):
    print('\n*** Gather information to generate Nextflow %s ***' % template_name.replace('-', ' '))

    project_dir = cookiecutter(
        os.path.join(GEN_HOME, template_name),
        config_file=config_file,
        no_input=no_input,
        extra_context=extra_context
    )

    config_dict = get_user_config(config_file=config_file)
    project_context = load(config_dict['replay_dir'], template_name)
    print('Template generated in: %s\n' % project_dir)

    return project_dir, project_context


def main(gen_type, commit=False, config_file=None, no_input=False, extra_context={}):
    project_dir = ''
    module_dir = ''
    cwd = os.getcwd()

    if gen_type in ('p', 'pm'):
        project_dir, project_context = template_gen(
            'project-template',
            config_file=config_file,
            no_input=no_input,
            extra_context=extra_context
        )

        # print(project_context)
        git_init_push(
            project_dir,
            project_context['cookiecutter']['github_account'],
            project_context['cookiecutter']['project_slug'],
            branch='main'
        )

    if gen_type in ('pm', 'm'):
        if project_dir:
            os.chdir(os.path.join(project_dir, 'tools'))

        module_dir, module_context = template_gen(
            'module-template',
            config_file=config_file,
            no_input=no_input,
            extra_context=extra_context
        )

        # print(module_context)
        module_name = module_context['cookiecutter']['module_name']
        module_version = module_context['cookiecutter']['module_version']
        branch = '%s.%s' % (module_name, module_version)
        git_commit_push(
            module_dir,
            branch,
            'commit with auto-generated module template for %s' % branch
        )

        docker_build_push(
            module_dir,
            module_context['cookiecutter']['quay_io_account'],
            module_name,
            branch
        )

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
    parser.add_argument('-n', '--no-input', dest='no_input', action='store_true',
                        help='No interactive input from prompt')
    parser.add_argument('-p', '--project-name', dest='project_name', type=str,
                        help='Project name')

    args = parser.parse_args()

    extra_context = {}
    if args.project_name:
        extra_context['project_name'] = args.project_name

    main(
        gen_type=args.gen_type,
        commit=args.commit,
        config_file=args.config_file,
        no_input=args.no_input,
        extra_context=extra_context
    )
