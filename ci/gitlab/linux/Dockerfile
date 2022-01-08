FROM MANYLINUX_DOCKER_CONTAINER

ENV SYSTEM_LIBSSH 1

COPY ./ci/gitlab/linux /scripts
COPY ./ci/build_ssh.sh /scripts/build_ssh.sh
COPY ./libssh /libssh

RUN /scripts/setup_manylinux.sh

# Libssh2
RUN mkdir -p build_libssh && cd build_libssh && \
    cmake -DCMAKE_BUILD_TYPE=Release -DWITH_NACL=ON -DWITH_PKCS11_URI=ON -DWITH_GSSAPI=ON -DWITH_BLOWFISH_CIPHER=ON /libssh && \
    make -j install

RUN rm -rf build_libssh
