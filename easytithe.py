#!/usr/bin/python

"""Library for EasyTithe Manager."""

__author__ = 'alex@rohichurch.org (Alex Ortiz-Rosado)'

import cookielib
import urllib2
import urllib


class LoginException(Exception):
  pass


class EasyTithe(object):
  def __init__(self, username, password):
    self.username = username
    self.password = password

    self.cookie_jar = cookielib.CookieJar()

    self.opener = urllib2.build_opener(
      urllib2.HTTPHandler(debuglevel=0),
      urllib2.HTTPSHandler(debuglevel=0),
      urllib2.HTTPErrorProcessor(), 
      urllib2.HTTPRedirectHandler(),
      urllib2.HTTPCookieProcessor(self.cookie_jar))

    self.opener.addheaders = [('User-agent', 
      ('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)'))]

  def login(self):
    login_data = urllib.urlencode({
      'login': self.username,
      'password': self.password,
      'submit': 'Login'
    })
    response = self.opener.open("https://www.easytithe.com/cp/default.asp", login_data)
    processed_cookies = [(cookie.name, cookie.value) for cookie in self.cookie_jar
                         if not cookie.is_expired()]
    self.cookies = dict(processed_cookies)
    if 'mbadlogin' in self.cookies:
      if self.cookies['mbadlogin'] == '1':
        raise LoginException("Login failure. Check username and password.")

  def get_report(self, start_date, end_date, export_csv=False):
    report_url = ('https://www.easytithe.com/cp/report-custom_dated-export.asp?'
                  'sdate=%s&edate=%s&organize=comment') % (start_date, end_date)
    report = self.opener.open(report_url).read()
    if export_csv:
      export_file = open('export.csv','w')
      export_file.write(report)
      export_file.close()
    else:
      print report
   

def main():
  username = '<username>'
  password = '<password>'

  et = EasyTithe(username, password)
  et.login()
  et.get_report('10/6/2013', '10/13/2013')


if __name__ == "__main__":
    main()





