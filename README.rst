# EfficientIP connector

Manage FortiManager objects with EfficientIP IPAM solution
The deamon can run directly with the command:

$ python3 -m connector IP_FMG IP_SOLIDserver adom fmg_user fmg_passwd ipam_user ipam_passwd sync_delete timer_refresh

 - IP_FMG: IPv4 FortiManager
 - IP_SOLIDserver: IPv4 SOLIDserver 
 - adom: adom to work with
 - fmg_user: FortiManager usernamme with API rights
 - fmg_passwd: FortiManager password
 - ipam_user: SOLIDserver usernamme
 - ipam_passwd: SOLIDserver password
 - sync_delete: delete object on FortiManager if not used. Object used by firewall policy or address group can't be force delete by API
 - timer_refresh: timer between each refresh

# How to use docker container

To change arguments you can either change it directly in the Dockerfile ("ARG" lines) or
build the container with specified argument like this:
  $ docker build --build-arg IP_FMG=192.168.1.1 \
    --build-arg IP_SOLIDserver=192.168.1.2 \
    -t connector .

Use the following command in Dockerfile folder to build the container:
  $ docker build -t connector .

Once it's done building, run the container with command:
  $ docker run --name demo -it connector