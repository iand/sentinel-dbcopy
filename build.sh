#!/bin/bash
docker build -t sentinel-dbcopy . 
docker tag sentinel-dbcopy thattommyhall/sentinel-dbcopy:latest 
docker push thattommyhall/sentinel-dbcopy:latest
