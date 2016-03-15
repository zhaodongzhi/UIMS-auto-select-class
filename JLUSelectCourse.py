#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cookielib
import urllib
import urllib2
from hashlib import md5
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class SelectCourse:
    def __init__(self):
        self.url_prefix = 'http://uims.jlu.edu.cn/ntms/'
        self.username = ''
        self.password = ''
        self.course_id = ''
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cookie))

    def login(self):
        LOGIN_URL = self.url_prefix + 'j_spring_security_check'
        PASSWORD_ENCRYPTED = \
            md5('UIMS' + self.username + self.password).hexdigest()
        login_data = {'j_username': self.username,
                      'j_password': PASSWORD_ENCRYPTED}
        self.opener.open(LOGIN_URL, urllib.urlencode(login_data))

    def selectCourse(self):
        print 'selecting...'
        while True:
            param = json.dumps({"lsltId": self.course_id,
                                "opType": "Y"}).encode('utf-8')
            content = {'Content-Type': 'application/json'}
            request = urllib2.Request(
                self.url_prefix + 'selectlesson/select-lesson.do',
                param, headers=content)
            response = self.opener.open(request)
            try:
                response = json.loads(response.read())
                stat = response['errno']
            except Exception:
                stat = None
            if stat == 1410:
                print 'Course select successfully!'
                return


if __name__ == '__main__':
    c = SelectCourse()
    c.login()
    c.selectCourse()

