#!/usr/bin/env nextflow

nextflow.enable.dsl=2  // enable DSL 2
version = '{{ cookiecutter.version }}'  // tool version

// universal params go here, change default value as needed
params.container_version = ""
params.cpus = 1
params.mem = 1  // GB
params.publish_dir = ""  // set to empty string will disable publishDir

// tool specific parmas go here, add / change as needed
params.input_file = ""
params.output_pattern = "*.txt"


process {{ cookiecutter.tool_name }} {
  container "quay.io/{{ cookiecutter.quay_io_account }}/{{ cookiecutter.tool_name }}:{{ cookiecutter.tool_name }}.${params.container_version ?: version}"
  publishDir "${params.publish_dir}/${task.process.replaceAll(':', '_')}", mode "copy", enabled: "${params.publish_dir ? true : ''}"

  cpus params.cpus
  memory "${params.mem} GB"

  input:  // input, make update as needed
    path input_file

  output:  // output, make update as needed
    path "output_dir/${params.output_pattern}", emit: output

  script:
    // add and initialize variables here as needed

    """
    mkdir -p output_dir

    {{ cookiecutter.tool_name }}.py \
      -i ${input_file} \
      -o output_dir

    """
}
