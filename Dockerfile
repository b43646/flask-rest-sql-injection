# base image
FROM docker.io/p0bailey/docker-flask:latest

# MAINTAINER
MAINTAINER loren@redhat.com

# running required command
RUN mkdir -p /opt/app
RUN cd /opt/app
RUN pip install flask_restful

ADD ./hack /opt/app/hack

WORKDIR /opt/app/hack


ENTRYPOINT [ "python", "main.py" ]
EXPOSE 5000
