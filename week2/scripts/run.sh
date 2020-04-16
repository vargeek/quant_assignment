#!/bin/bash

set -e

cd $(cd $(dirname $0); pwd)/../build

nohup ./quant >logs/logs 2>&1 &
