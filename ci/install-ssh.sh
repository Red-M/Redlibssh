#!/bin/bash -xe

if [ -d /usr/local/opt/openssl ]; then
    export OPENSSL_ROOT_DIR=/usr/local/opt/openssl
fi

mkdir -p src && cd src

if [ "$(uname)" == "Darwin" ];then
    MACOS_DETECTED="asdsdgsdfg"
fi

if [ ! -z $MACOS_DETECTED ]; then
    MACOS_ARGS="-DCMAKE_OSX_SYSROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX${MACOSX_DEPLOYMENT_TARGET}.sdk/ -DCMAKE_OSX_DEPLOYMENT_TARGET=${MACOSX_DEPLOYMENT_TARGET}"
fi
if [ ! -z $MACOS_DETECTED ]; then
    cmake ../libssh -DWITH_NACL=ON -DWITH_PKCS11_URI=ON -DWITH_GSSAPI=ON -DWITH_BLOWFISH_CIPHER=ON -DCMAKE_INSTALL_PREFIX=../ ${MACOS_ARGS}
else
    cmake ../libssh -DWITH_NACL=ON -DWITH_PKCS11_URI=ON -DWITH_GSSAPI=ON -DWITH_BLOWFISH_CIPHER=ON -DCMAKE_INSTALL_PREFIX=../
fi
make -j all install
