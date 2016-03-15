#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent
from gevent import monkey
# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()

import cookielib
import urllib
import urllib2
from hashlib import md5
import json
import argparse
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class SelectCourse:
    def __init__(self, username, password):
        self.url_prefix = 'http://uims.jlu.edu.cn/ntms/'
        self.username = username
        self.password = password
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

    def selectCourse(self, courseid):
        print 'selecting...'
        while True:
            param = json.dumps({"lsltId": courseid,
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
                print courseid, 'select successfully!'
                return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JLU auto select course')
    parser.add_argument("-username", action="store", dest="username",
                        type=str, required=True)
    parser.add_argument("-password", action="store", dest="password",
                        type=str, required=True)
    parser.add_argument("-courseid", action="append", dest="courseids",
                        type=str, required=True)
    given_args = parser.parse_args()
    username = given_args.username
    password = given_args.password
    courseids = given_args.courseids
    thread_nums = len(courseids) * 4
    select_course = SelectCourse(username, password)
    select_course.login()
    jobs = [gevent.spawn(select_course.selectCourse,
                         courseids[i % len(courseids)])
            for i in xrange(thread_nums)]
    gevent.joinall(jobs)
