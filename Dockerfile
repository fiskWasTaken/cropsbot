FROM bamos/openface
MAINTAINER fisk <myself@fiskie.me>

COPY src /root/lewdcrops

# Install python deps from requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

CMD cd /root/lewdcrops; ./main.py