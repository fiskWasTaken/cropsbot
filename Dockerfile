FROM bamos/openface
MAINTAINER fisk <myself@fiskie.me>

COPY crontab /etc/cron.d/lewdcrops

COPY src /root/lewdcrops

# Install python deps from requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

EXPOSE 8000 9000
CMD /bin/bash -l -c '/root/openface/demos/web/start-servers.sh'