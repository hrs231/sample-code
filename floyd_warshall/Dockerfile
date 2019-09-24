# Building from base os level
FROM ubuntu as intermediate

# install git
RUN apt-get update
RUN apt-get install -y git

RUN git clone https://github.com/hrs231/sample-code.git

FROM python:alpine3.7

# copy the repository form the previous image
COPY --from=intermediate /sample-code/floyd_warshall /floyd_warshall

# Actual scripts to be triggered 
WORKDIR /floyd_warshall

# Update any requirements (currently none, so just uncomment this if needed )
COPY --from=intermediate /sample-code/floyd_warshall/requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

# The commands to run each time
# RUN /bin/bash -c "source ./.env"
ENV PYTHONPATH "${PYTHONPATH}:/floyd_warshall"

# Need to run the flask app
CMD python ./index.py
