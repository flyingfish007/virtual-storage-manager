#!/bin/bash

# Copyright 2014 Intel Corporation, All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the"License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

#-------------------------------------------------------------------------------
#            Usage
#-------------------------------------------------------------------------------

function usage() {
    cat << EOF
Usage: $0

Build VSM Release Package:
    The tool can help to pull all necessary documents, binaries into one place,
    and maintain an expected folder structure, then generate a release package.

Options:
  --help | -h
    Print usage information.
EOF
    exit 0
}

while [ $# -gt 0 ]; do
  case "$1" in
    -h) usage ;;
    --help) usage ;;
    *) shift ;;
  esac
  shift
done

set -e
set -o xtrace

TOPDIR=$(cd $(dirname "$0") && pwd)
TEMP=`mktemp`; rm -rfv $TEMP >/dev/null; mkdir -p $TEMP;
#DATE=`date "+%Y%m%d"`

VERSION=`cat VERSION`
export VERSION
RELEASE=`cat RELEASE`
export RELEASE
BUILD="${VERSION}.${RELEASE}"

is_lsb_release=0
lsb_release -a >/dev/null 2>&1 && is_lsb_release=1

if [[ $is_lsb_release -gt 0 ]]; then
    OS=`lsb_release -a|grep "Distributor ID:"|awk -F ' ' '{print $3}'`
    OS_VERSION=`lsb_release -a|grep "Release"|awk -F ' ' '{print $2}'`
else
    var=`cat /etc/os-release|grep "PRETTY_NAME"|awk -F "=" '{print $2}'`
    if [[ $var =~ "CentOS Linux 7" ]]; then
        OS="CentOS"
        OS_VERSION="7"
    fi
fi

TEMP_VSM=`mktemp`; rm -rfv $TEMP_VSM >/dev/null; mkdir -p $TEMP_VSM;
mkdir -p $TEMP_VSM/release/$BUILD
cp -rf * $TEMP_VSM
cp -rf .lib $TEMP_VSM
if [ -d ubuntu14/.lib ]; then
    cp -rf ubuntu14/.lib $TEMP_VSM/ubuntu14/.lib
fi
cd $TEMP_VSM

function create_release() {
    if [[ $OS == "Ubuntu" && $OS_VERSION =~ "14" ]]; then
        cp -rf ubuntu14/.lib .
        cp -rf ubuntu14/python-vsmclient ./source
        cp -rf ubuntu14/vsm ./source
        cp -rf ubuntu14/vsm-dashboard ./source
        cp -rf ubuntu14/vsm-deploy ./source
        cp ubuntu14/builddeb .
        bash +x builddeb
        cp ubuntu14/install.sh release/$BUILD
        cp ubuntu14/uninstall.sh release/$BUILD
        cp ubuntu14/upgrade.sh release/$BUILD
        cp ubuntu14/debs.lst release/$BUILD
    elif [[ $OS == "CentOS" && $OS_VERSION =~ "7" ]]; then
        bash +x buildrpm
        cp install.sh release/$BUILD
    fi

    cp VERSION release/$BUILD
    cp RELEASE release/$BUILD
    cp README.md release/$BUILD
    cp INSTALL.md release/$BUILD
    cp LICENSE release/$BUILD
    cp NOTICE release/$BUILD
    cp CHANGELOG.md release/$BUILD
    cp installrc release/$BUILD
#    cp -r manifest release/$BUILD
    mkdir -p release/$BUILD/manifest
    cp source/vsm/etc/vsm/cluster.manifest release/$BUILD/manifest/cluster.manifest.sample
    cp source/vsm/etc/vsm/server.manifest release/$BUILD/manifest/server.manifest.sample
    cp -r vsmrepo release/$BUILD

    cd release
    tar -czvf $BUILD.tar.gz $BUILD
    rm -rf $BUILD
    cp -r $TEMP_VSM/release $TOPDIR
    cp -r $TEMP_VSM/vsmrepo $TOPDIR

}

create_release

rm -rf $TEMP_VSM

cd ${TOPDIR}
echo -n $((++RELEASE)) > RELEASE

set +o xtrace

