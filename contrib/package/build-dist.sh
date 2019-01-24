#!/usr/bin/env bash

set -e # Exit script if anything fails
set -u # unset variables cause an error
set -o pipefail # https://coderwall.com/p/fkfaqq/safer-bash-scripts-with-set-euxo-pipefail
#set -x # for debugging each command

ROOT_DIR=$(git rev-parse --show-toplevel)
cd ${ROOT_DIR}

TARGET_DIR="${ROOT_DIR}/target/dist"
LIB_DIR="${TARGET_DIR}/lib"
CONTRACT_DIR="${TARGET_DIR}/contracts"


echo "Going to build a chainspace distribution in ${TARGET_DIR} ... "

rm -rf ${TARGET_DIR}
mkdir -p ${TARGET_DIR} ${LIB_DIR} ${CONTRACT_DIR}


CHAINSPACE_APP_JAR=`ls ${ROOT_DIR}/chainspacecore/target/chainspace*-with-dependencies.jar`
BFT_JAR=`ls ${ROOT_DIR}/chainspacecore/lib/bft-smart*-DECODE.jar`
NODE_CONFIG_TEMPLATE="${ROOT_DIR}/contrib/package/node-config-template"
BIN_DIR="${ROOT_DIR}/contrib/package/bin"
EXAMPLE_NETWORKS_DIR="${ROOT_DIR}/contrib/package/example-networks"

CONTRACT_SRC_DIR="${ROOT_DIR}/chainspacecore/contracts"

echo -e "Copying files accross..."
cp ${CHAINSPACE_APP_JAR} ${LIB_DIR}
cp ${BFT_JAR} ${LIB_DIR}
cp ${CONTRACT_SRC_DIR}/* ${CONTRACT_DIR}

cp -r ${NODE_CONFIG_TEMPLATE} ${TARGET_DIR}

cp ${BIN_DIR}/* ${TARGET_DIR}
cp -r ${EXAMPLE_NETWORKS_DIR} ${TARGET_DIR}


cd ${TARGET_DIR}

if hash tree 2>/dev/null; then
    tree --dirsfirst
fi
cd -

echo -e "\nCompleted building of the distribution.\n"

