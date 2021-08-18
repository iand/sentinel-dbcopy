FROM filecoin/sentinel-visor:v0.7.5

RUN apt update && apt install -y postgresql-client python3 python3-pip unzip csvkit
RUN pip3 install pendulum paramiko pyyaml
#RUN pip3 install "dask[dataframe]"
#RUN pip3 install "dask[distributed]"

RUN wget -O - https://github.com/peak/s5cmd/releases/download/v1.2.1/s5cmd_1.2.1_Linux-64bit.tar.gz  | tar -xz -C /usr/bin/ s5cmd

RUN wget https://downloads.rclone.org/v1.55.1/rclone-v1.55.1-linux-amd64.zip && unzip -j rclone-v1.55.1-linux-amd64.zip rclone-v1.55.1-linux-amd64/rclone -d /usr/bin/

ADD airflow ./airflow

ENTRYPOINT []
