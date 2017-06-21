#!/bin/bash

mdb-export -b strip -X '\' -D '%Y-%m-%d %H:%M:%S' ./data/kea_be.mdb "tStudyAreas" > "data/tStudyAreas.csv"
mdb-export -b strip -X '\' -D '%Y-%m-%d %H:%M:%S' ./data/kea_be.mdb "Kea" > "data/Kea.csv"
mdb-export -b strip -X '\' -D '%Y-%m-%d %H:%M:%S' ./data/kea_be.mdb "Transmitter actions" > "data/Transmitter actions.csv"
