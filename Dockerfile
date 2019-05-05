# base image
FROM docker.io/p0bailey/docker-flask:latest

# MAINTAINER
MAINTAINER loren@redhat.com

# running required command
RUN mkdir -p /opt/app
RUN cd /opt/app
RUN pip install flask_restful

ADD ./hackable /opt/app/hackable

WORKDIR /opt/app/hackable


ENTRYPOINT [ "python", "main.py" ]
EXPOSE 5000
