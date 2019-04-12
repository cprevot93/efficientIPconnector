# -*- coding: utf-8 -*-

from connector import helpers

ip_FMG = "10.10.20.254"
user ='admin'
passwd ='AdminFMG'
adom = "global"
helpers.api.login(ip_FMG, user, passwd)
helpers.api.debug('off')
