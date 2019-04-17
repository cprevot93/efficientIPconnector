# -*- coding: utf-8 -*-

from connector import helpers

ip_FMG = "100.68.99.10"
user ='admin'
passwd ='fortinet'
adom = "root"
helpers.api.login(ip_FMG, user, passwd)
helpers.api.debug('off')
