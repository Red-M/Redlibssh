#!/bin/bash -xe

PYTHON_DIR=${1:-python}
PYTHON_BIN=${2:-python}

OLD_PWD="$(pwd)"
LATEST_PY="$(ls -1d /opt/${PYTHON_DIR}/*/bin | grep -v cpython | tail -n1)/${PYTHON_BIN}"
cd /io
"${LATEST_PY}" /io/setup.py sdist -d /io/wheelhouse --formats=gztar

# Compile wheels
for PYBIN in `ls -1d /opt/${PYTHON_DIR}/*/bin | grep -v cpython`; do
    "${PYBIN}/pip" wheel /io/wheelhouse/*.gz -w /tmp/wheelhouse/
done
cd "${OLD_PWD}"

"${LATEST_PY}" -m pip install -U auditwheel

# Bundle external shared libraries into the wheels
for whl in /tmp/wheelhouse/*.whl; do
    auditwheel repair "${whl}" -w /io/wheelhouse/
    \rm "${whl}"
done

# Install packages and test
for PYBIN in `ls -1d /opt/${PYTHON_DIR}/*/bin | grep -v cpython`; do
    "${PYBIN}/pip" install redlibssh --no-index -f /io/wheelhouse
    (cd "${HOME}"; "${PYBIN}/${PYTHON_BIN}" -c 'import ssh; ssh.session.Session(); print(ssh.__version__); print(ssh.utils.openssl_version_text)')
done
