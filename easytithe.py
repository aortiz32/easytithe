#!/usr/bin/python

"""Python library for Easy Tithe Manager.

Easy Tithe is an online giving platform for churches and organizations that
makes accepting, tracking and reporting online tithing and donations, well...
easy.

The Easy Tithe Manager includes a range of reports, which can be viewed by
person, transaction, fund and date ranges. Access to the Easy Tithe Manager
is done through the Easy Tithe website at
https://www.easytithe.com/cp/default.asp.

Easy Tithe library provides an API for logging into the Easy Tithe Manager
and accessing reports.

Usage:
  import easytithe
  
  et = easytithe.EasyTithe('username', 'passsword')
  et.login()
  csv_report_data = et.get_report(
    start_date='10/6/2013',
    end_date='10/13/2013')
  print csv_report_data
"""

__author__ = 'alex@rohichurch.org (Alex Ortiz-Rosado)'

import cookielib
import csv
import json
import urllib
import urllib2


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
    return report

def csv_to_json(csvfile):
	"""Utility for converting a CSV file to JSON-formatted output."""
	f = open(csvfile, 'r')
	reader = csv.reader(f, delimiter=',', quotechar='"')
	# skip the headers and any HTML comments
	row = next(reader)
	while any('<!--' in r for r in row):
		row = next(reader)
	keys = row
	out = [{key: val for key, val in zip(keys, prop)} for prop in reader]
	return json.dumps(out, sort_keys = False, indent = 1)
	
def main():
  username = '<username>'
  password = '<password>'

  et = EasyTithe(username, password)
  et.login()
  start_date = '9/8/2013'
  end_date = '9/17/2013'
  report = et.get_report(start_date, end_date, export_csv=True)
  print("Easy Tithe Report for: %s to %s in CSV format\n%s") % (
      start_date, end_date, report)
  print("Easy Tithe Report for %s to %s in JSON format\n%s") % (
      start_date, end_date, csv_to_json('export.csv')) 


if __name__ == "__main__":
    main()
