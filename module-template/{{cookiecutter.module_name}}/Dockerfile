FROM {{ cookiecutter.docker_base_image }}

ENV PATH="/tools:${PATH}"

COPY *.py /tools/

RUN groupadd -g 1000 ubuntu &&\
    useradd -l -u 1000 -g ubuntu ubuntu &&\
    install -d -m 0755 -o ubuntu -g ubuntu /home/ubuntu

USER ubuntu

CMD ["/bin/bash"]
