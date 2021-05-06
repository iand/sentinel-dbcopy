#!/bin/bash
set -u
set -e
rm -rf /repo/*
s5cmd cp --if-size-differ "${S3_REPO_PATH}/*" /repo/
CSV_PATH="/output/${JOB_NAME}/${VISOR_HEIGHT_FROM}__${VISOR_HEIGHT_TO}"
mkdir -p "${CSV_PATH}"
rm -f "${CSV_PATH}/*.csv"
/usr/bin/visor --repo-read-only=false --lens lotusrepo --repo /repo --db "" walk --csv "${CSV_PATH}"
