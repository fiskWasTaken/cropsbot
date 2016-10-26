FROM bamos/openface
MAINTAINER fisk <myself@fiskie.me>

# Install python deps from requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

CMD echo "To use this image, mount your script and override --entrypoint. e.g. 'docker run --entrypoint python /root/your-script'"
