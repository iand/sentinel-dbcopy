FROM filecoin/sentinel-visor:master-93f752ef

RUN apt update && apt install -y postgresql-client python3 python3-pip
RUN pip3 install pendulum

RUN wget -O - https://github.com/peak/s5cmd/releases/download/v1.2.1/s5cmd_1.2.1_Linux-64bit.tar.gz  | tar -xz -C /usr/bin/ s5cmd

ADD *.py ./

ADD run_backfill.sh .
RUN chmod a+x run_backfill.sh

ENTRYPOINT []
