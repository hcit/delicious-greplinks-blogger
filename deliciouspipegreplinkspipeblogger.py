#!/usr/bin/env python
# -*- coding: utf-8-unix -*-

"""
File: deliciouspipegreplinkspipeblogger.py
Author: Jonas Gorauskas [JGG]
Description: 
  Looks up the delicious links I posted recently and generates
  a blog post for blogger from the links.
Created: 2010-10-09 04:12:16

History:

    2010-10-09 04:12:50 - JGG
        Initial version

copyright (c) MMX Jonas Gorauskas
"""


from pydelicious import DeliciousAPI
from gdata.blogger.client import BloggerClient
from time import mktime
from datetime import datetime
from optparse import OptionParser
from ConfigParser import SafeConfigParser, RawConfigParser


class DeliciousHelper(object):
    """
    Helper class for the delicious api
    """
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._api = DeliciousAPI(self._username, self._password)

    def get_last_update(self):
        dt = datetime.fromtimestamp(mktime(self._api.posts_update()['update']['time']))
        return dt

    def get_recent_links(self, dt):
        l = []
        
        for link in self._api.posts_recent(count=30)['posts']:
            pdt = datetime.strptime(link['time'], '%Y-%m-%dT%H:%M:%SZ')
            if pdt > dt:
                l.append(link)
        
        return l


class BloggerHelper(object):
    """
    Helper class for the Blogger GData API
    """
    def __init__(self, username, password, blog_id):
        self._username = username
        self._password = password
        self._blog_id = blog_id
        self._client = BloggerClient()

    def create_post(self, title, content, is_draft):
        lbls = ['Links', 'Cool Stuff']
        
        self._client.client_login(self._username,
                                  self._password,
                                  source='Delicious2Blogger - v0.1.2',
                                  service='blogger')
        
        self._client.add_post(self._blog_id,
                              title,
                              content,
                              draft=is_draft,
                              labels=lbls)


class Settings(object):
    """
    Parse the command line and the INI file and initialize the whole thing.
    Holds the settings that will drive the process
    """
    def __init__(self):
        p = OptionParser(usage=r'usage: %prog [options] arg',
                         version='%prog - version 0.1.2 - beta',
                         description='Looks up the delicious links posted recently to your account and generates a blog post for blogger from the links.',
                         epilog='Requires the pydelicious and blogger data api modules. http://code.google.com/p/pydelicious/      http://code.google.com/apis/blogger/')

        p.add_option('-v', '--verbose',
                     dest='verbose', action='store_true',
                     help='display and log verbose messages [default]',
                     default=True)
        p.add_option('-q', '--quiet',
                     dest='verbose', action='store_false',
                     help='turns verbosity way down')
        p.add_option('-l', '--log',
                     dest='log', action='store_true',
                     help='write messages to a log file')
        p.add_option('-i', '--inifile',
                     dest='inifile', metavar='FILE', default='deliciouspipegreplinkspipeblogger.ini',
                     help='the configuration file that drives the work')
        
        options, arguments = p.parse_args()
        config = SafeConfigParser()
        config.read(options.inifile)        
        
        self.verbose = options.verbose
        self.log = options.log
        self.ini_file = options.inifile
        self.log_file = config.get('Main', 'logfile')
        self._last_update = config.get('Main', 'lastupdate')
        self.delicious_username = self._rot13(config.get('Delicious', 'username'))
        self.delicious_password = self._rot13(config.get('Delicious', 'password'))
        self.blogger_username = self._rot13(config.get('Blogger', 'username'))
        self.blogger_password = self._rot13(config.get('Blogger', 'password'))
        self.blog_id = config.get('Blogger', 'blogid')
        self.post_title_template = config.get('Blogger', 'posttitletmp')
        
    def get_last_update(self):
        dt = datetime.fromtimestamp(float(self._last_update))
        return dt

    def set_last_update(self, dt):
        tt = dt.timetuple()
        ts = mktime(tt)
        self._last_update = str(ts)
        
        config = RawConfigParser()
        config.read(self.ini_file)
        config.set('Main', 'lastupdate', self._last_update)
        inifile = open(self.ini_file, 'wb')
        config.write(inifile)
        inifile.close()

    _d = {}
    def _rot13(self, text):
        if not self._d:
            for c in (65, 97):
                for i in range(26):
                    self._d[chr(i + c)] = chr((i + 13) % 26 + c)
                
        return ''.join([self._d.get(c, c) for c in text])    


def build_post_body(links):
    html = '<p>\n'.encode('utf-8')

    for link in links:
        html += ' <a href="'.encode('utf-8')
        html += link['href'].encode('utf-8')
        html += '">'.encode('utf-8')
        html += link['description'].encode('utf-8')
        html += '</a><br/>\n'.encode('utf-8')
    
    html += '</p>\n'.encode('utf-8')
    return html


def write(msg, settings):
    """Writes a message to the log file and/or to the screen"""
    if settings.verbose:
        print msg

    if settings.log:
        encoded_msg = msg.encode('utf-8')
        encoded_dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')
        out = '%s %s\n' % (encoded_dt, encoded_msg)
        f = open(settings.log_file, 'a')
        f.write(out)
        f.close()


def main():
    s = Settings()
    write('START Delicious Pipe Grep Links Pipe Blogger', s)
    write(' Connecting to delicious', s)
    dh = DeliciousHelper(s.delicious_username, s.delicious_password)
    bh = BloggerHelper(s.blogger_username, s.blogger_password, s.blog_id)

    if dh.get_last_update() > s.get_last_update():
        write(' There is work to do', s)
        write(' Get recent links', s)
        links = dh.get_recent_links(s.get_last_update())
        write(' There are %d links to process' % len(links), s)
        write(' Building post title', s)
        title = s.post_title_template + ' ' + datetime.now().strftime('%Y-%m-%d').encode('utf-8')
        write(' Building post content', s)
        content = build_post_body(links)
        write(' Creating post', s)
        bh.create_post(title, content, False)
        write(' Created post success', s)
    else:
        write(' There is no work to do', s)

    s.set_last_update(datetime.now())
    write('FINISH Delicious Pipe Grep Links Pipe Blogger', s)


if __name__ == '__main__':
    main()

