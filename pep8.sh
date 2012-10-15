#!/bin/bash

echo -e "\nRunning: (pep8 --show-source --show-pep8 --select=errors --testsuite=.)\n\n"
pep8 --show-source --show-pep8 --select=errors --testsuite=./
echo -e "\n\n"
