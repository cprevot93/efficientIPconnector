#
# Author: Charles Prevot - Fortinet
# Date: 04/2019
#
FROM python:3.7.3
LABEL author="Charles Prevot"
LABEL maintainer="cprevot@fortinet.com"
LABEL version="0.1"

ENV lib ftntlib-0.4.0.dev13

# FMG IP
ARG IP_FMG=100.68.99.10
ENV IP_FMG=${IP_FMG}

# SOLIDserver IP
ARG IP_SOLIDserver=100.68.99.20
ENV IP_SOLIDserver=${IP_SOLIDserver}

# ADOM to work with
ARG adom=root
ENV ADOM=${adom}

# FMG user
ARG fmg_user=admin
ENV FMG_USER=${fmg_user}

# FMG pass
ARG fmg_passwd=fortinet
ENV FMG_PASSWD=${fmg_passwd}

# SOLIDserver user
ARG ipam_user=ipmadmin
ENV IPAM_USER=${ipam_user}

# SOLIDserver pass
ARG ipam_passwd=admin
ENV IPAM_PASSWD=${ipam_passwd}

# Delete object on FMG
# If =1 -> object unused be group or policy group will be deleted
ARG sync_delete=1
ENV SYNC_DELETE=${sync_delete}

# Timer between each sync in MIN
ARG time_refresh=1
ENV TIME_REFRESH=${time_refresh}

WORKDIR /opt
ADD requirements.txt .
ADD connector/ connector
ADD $lib/ $lib
RUN pip install -r requirements.txt
RUN cd ${lib} && python setup.py install
CMD python -m connector ${IP_FMG} ${IP_SOLIDserver} ${ADOM} ${FMG_USER} ${FMG_PASSWD} ${IPAM_USER} ${IPAM_PASSWD} ${SYNC_DELETE} ${TIME_REFRESH}
