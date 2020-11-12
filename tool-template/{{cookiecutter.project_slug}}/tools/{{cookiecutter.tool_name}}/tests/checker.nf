#!/usr/bin/env nextflow

/*
 This is an auto-generated checker workflow, please update as needed
*/

nextflow.enable.dsl = 2  // enable DSL 2
version = '{{ cookiecutter.version }}'  // tool version

// universal params
params.publish_dir = ""

// tool specific parmas go here, add / change as needed
params.input_file = ""
params.expected_output = ""

include { {{ cookiecutter.tool_name }} } from '../{{ cookiecutter.tool_name }}'

Channel
  .fromPath(params.input_file, checkIfExists: true)
  .set { input_file }


process file_diff {
  container "quay.io/{{ cookiecutter.quay_io_account }}/{{ cookiecutter.tool_name }}:{{ cookiecutter.tool_name }}.${params.container_version ?: version}"

  input:
    path file1
    path file2

  output:
    stdout out

  script:
    """
    diff ${file1} ${file2}

    echo $?
    """
}


workflow checker {
  take:
    input_file
    expected_output

  main:
    {{ cookiecutter.tool_name }}(
      input_file
    )

    file_diff(
      {{ cookiecutter.tool_name }}.out.output,
      expected_output
    )

    if (file_diff.out.out == '0') {
      exit 0, "Test PASS"
    } else {
      exit 1, "Test FAILED"
    }
}


workflow {
  checker(
    file(params.input_file),
    file(params.expected_output)
  )
}
