# -*- coding: utf-8 -*-

from connector import helpers

helpers.api.debug('off')
ip_FMG = "100.68.99.10"
fmg_user ='admin'
fmg_passwd ='fortinet'
adom = "root"

ip_SOLIDserver = "100.68.99.20"
ipam_user = "ipmadmin"
ipam_passwd = "admin"
helpers.api.login(ip_FMG, fmg_user, fmg_passwd)