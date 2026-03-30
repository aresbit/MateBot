#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
source /home/ares/yyshm/env.sh

echo "JAVA:"
java -version 2>&1 | head -n 1

echo "NODE:"
node -v

echo "NPM:"
npm -v

echo "HDC:"
hdc version

echo "HVIGORW:"
hvigorw -v

echo "OHPM:"
ohpm -v

echo "CODELINTER:"
codelinter -v

echo "HSTACK:"
hstack --version

echo "TARGETS:"
hdc list targets
