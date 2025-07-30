FROM ubuntu:24.04

ARG dir_software="/app/Software"
WORKDIR ${dir_software}
USER root

RUN apt update && apt install -y zip unzip wget curl net-tools x11-apps\
    nano git openssh-client &&\
    mkdir -p /root/.ssh &&\
    ssh-keyscan github.com >> /root/.ssh/known_hosts

COPY install_simpleElastix.sh ${dir_software}/install_simpleElastix.sh
RUN --mount=type=ssh bash ${dir_software}/install_simpleElastix.sh