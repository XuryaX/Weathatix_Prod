__author__ = 'shaur'

import urllib2

def get_api_data(url):
    f = urllib2.urlopen(url)
    data_string = f.read()
    f.close()
    return data_string
