FROM python:3
ENV lib ftntlib-0.4.0.dev13

ARG IP_FMG=100.68.99.10
ENV IP_FMG=${IP_FMG}

ARG IP_SOLIDserver=100.68.99.20
ENV IP_SOLIDserver=${IP_SOLIDserver}

ARG adom=root
ENV ADOM=${adom}

ARG fmg_user=admin
ENV FMG_USER=${fmg_user}

ARG fmg_passwd=fortinet
ENV FMG_PASSWD=${fmg_passwd}

ARG ipam_user=ipmadmin
ENV IPAM_USER=${ipam_user}

ARG ipam_passwd=admin
ENV IPAM_PASSWD=${ipam_passwd}}

WORKDIR /opt
ADD requirements.txt .
ADD connector/ connector
ADD $lib/ $lib
RUN pip install -r requirements.txt
RUN cd ftntlib-0.4.0.dev13 && python setup.py install
CMD python -m connector ${IP_FMG} ${IP_SOLIDserver} ${ADOM} ${FMG_USER} ${FMG_PASSWD} ${IPAM_USER} ${IPAM_PASSWD}
