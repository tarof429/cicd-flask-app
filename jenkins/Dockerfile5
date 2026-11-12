# syntax=docker/dockerfile:1

ARG IMAGE_TAG="2.590-jdk21"

FROM jenkins/jenkins:${IMAGE_TAG}

USER root

# Update cache
RUN apt update

RUN apt install -y wget gnupg

# For trivy, force apt to use gpg instead of sqv
# See https://github.com/gluster/glusterfs/issues/4664
# RUN echo 'APT::Key::GPGCommand "/usr/bin/gpg";' > /etc/apt/apt.conf.d/99use-gpg-not-sqv \
#     && mkdir /etc/gnupg \
#     && echo "weak-digest SHA1" >> /etc/gnupg/gpg.conf \
#     && apt update

# Install trivy package
RUN  wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | tee /usr/share/keyrings/trivy.gpg > /dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" | tee -a /etc/apt/sources.list.d/trivy.list \
    && apt update \
    && apt install -y trivy

# Install ansible
RUN apt install -y ansible

# Install Docker
RUN install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg \
        -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(. /etc/os-release && echo "${VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

RUN apt update \
    && apt install -y --no-install-recommends \
        docker-ce-cli \
        docker-compose-plugin \
        docker-buildx-plugin

# Cleanup apt cache and other files
RUN rm -rf /var/lib/apt/lists/*

USER jenkins

#CMD ["tail", "-f", "/dev/null"]