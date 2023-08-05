#! /bin/bash

awk -F"time=" '/time=/{print $2}' ping_output.txt | awk -F" " '{sum += $1} END {print sum/NR}'
