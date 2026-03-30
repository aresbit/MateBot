#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/home/ares/yyshm"
ENV_SH="${BASE_DIR}/env.sh"
ZSHRC="/home/ares/.zshrc"

mkdir -p "${BASE_DIR}"
cat > "${ENV_SH}" <<'EOS'
# HarmonyOS Command Line Tools environment for Linux
export COMMANDLINE_TOOL_DIR=/home/ares/yyshm
export NODE_HOME=${COMMANDLINE_TOOL_DIR}/command-line-tools/tool/node
export HDC_HOME=${COMMANDLINE_TOOL_DIR}/command-line-tools/sdk/default/openharmony/toolchains
export PATH=${COMMANDLINE_TOOL_DIR}/command-line-tools/bin:${NODE_HOME}/bin:${HDC_HOME}:$PATH
EOS

if [ ! -f "${ZSHRC}" ]; then
  touch "${ZSHRC}"
fi
if ! grep -Fq 'source /home/ares/yyshm/env.sh' "${ZSHRC}"; then
  printf '\n# HarmonyOS CLI env\nsource /home/ares/yyshm/env.sh\n' >> "${ZSHRC}"
fi

# Load env for this execution
# shellcheck disable=SC1090
source "${ENV_SH}"

# Tool registries (from Huawei guide)
npm config set registry https://repo.huaweicloud.com/repository/npm/
npm config set "@ohos:registry" https://repo.harmonyos.com/npm/
ohpm config set registry https://ohpm.openharmony.cn/ohpm/
ohpm config set strict_ssl false

# Avoid ohpm trace-path warnings in fresh Linux hosts
mkdir -p /home/ares/Library/Caches/Huawei/DevEcoStudio6.0/TraceLogData

echo "[ok] HarmonyOS CLI environment configured at ${BASE_DIR}"
