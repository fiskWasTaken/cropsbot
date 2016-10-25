FROM bamos/openface
MAINTAINER fisk <myself@fiskie.me>

COPY src /root/lewdcrops

# Install python deps from requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# cron
COPY crontab /etc/cron.d/lewdcrops
RUN chmod 0644 /etc/cron.d/lewdcrops

RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log