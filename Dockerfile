FROM filecoin/sentinel-visor:master-93f752ef

RUN apt update && apt install -y postgresql-client python3 python3-pip
RUN pip3 install pendulum

ADD *.py ./

ENTRYPOINT []
