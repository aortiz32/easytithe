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
and accessing contribution data.

Usage:
  import easytithe

  et = easytithe.EasyTithe('username', 'passsword')
  contributions = et.GetContributions(
    start_date='10/6/2013',
    end_date='10/13/2013')
  print contributions
"""

__author__ = 'alexortizrosado@gmail.com (Alex Ortiz-Rosado)'

import cookielib
import csv
import urllib
import urllib2
from HTMLParser import HTMLParser


class LoginException(Exception):
    pass


class _TransferLoginParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.data = []

  def handle_starttag(self, tag, attributes):
    if tag != 'input':
      return
    self.data.append(dict(attributes))


class EasyTithe(object):
  """Class for EasyTithe giving platform."""
  def __init__(self, username, password):
    self.cookie_jar = cookielib.CookieJar()

    self.opener = urllib2.build_opener(
        urllib2.HTTPHandler(debuglevel=0),
        urllib2.HTTPSHandler(debuglevel=0),
        urllib2.HTTPCookieProcessor(self.cookie_jar))

    self.opener.addheaders = [(
        'User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                       'Windows NT 5.2; .NET CLR 1.1.4322)'))]
    self._Login(username, password)

  def _GetCookiesAsDict(self):
    """Returns all cookies as dictionary."""
    cookies = [(cookie.name, cookie.value) for cookie in self.cookie_jar
               if not cookie.is_expired()]
    return dict(cookies)

  def _TransferLogin(self, username, password_hash):
      """Secondary login for setting CSRF Token."""
      transfer_login_data = urllib.urlencode({
          'login': username,
          'ph': password_hash
      })

      self.opener.open(
          'https://www.easytithe.com/cp3o/Account/TransferLogin',
          transfer_login_data)

  def _Login(self, username, password):
    """Initial login form."""
    login_data = urllib.urlencode({
        'login': username,
        'password': password,
        'submit': 'Login'
    })
    response = self.opener.open(
        'https://www.easytithe.com/cp/default.asp',
        login_data)

    cookies = self._GetCookiesAsDict()
    if 'mbadlogin' in cookies:
      if cookies['mbadlogin'] == '1':
        raise LoginException('Login failure. Check username and password.')

    parser = _TransferLoginParser()
    parser.feed(response.read())
    parser.close()
    transfer_login_data = parser.data

    for t in transfer_login_data:
      if t['name'] != 'ph':
        continue
      password_hash = t['value']

    self._TransferLogin(username, password_hash)

  def GetContributions(self, start_date, end_date):
    """Returns a list of contributions.

    Args:
      start_date: Starting date range.
      end_date: Ending date range.

    Returns:
      List of contributions as dict:
        [
          {
            'Name': 'John Doe',
            'Phone': '4085551234',
            'Env Num': '',
            'Fund': 'Offering',
            'Amount': '$50.00',
            'Txn ID #': '5555551',
            'Address': '1234 Main St // San Jose, CA 95135',
            'Date': '5/31/2015 11:30:16 AM',
            'Type': 'Card-5555 Visa',
            'Email': 'jdoe555@yahoo.com'
          },
          {
            'Name': 'Jane Types',
            'Phone': '+14085555678',
            'Env Num': '',
            'Fund': 'Tithes',
            'Amount': '$250.00',
            'Txn ID #': '5555552',
            'Address': '5555 Acme Drive // San Jose, CA 95138',
            'Date': '5/31/2015 1:02:33 PM',
            'Type': 'Card-4455 Visa',
            'Email': 'janetypes@gmail.com'
          }
        ]

    """
    data = urllib.urlencode({
        'bdate': start_date,
        'edate': end_date,
        'organizesort': 'datestamp'
    })
    url = ('https://www.easytithe.com/cp3o/Reports/Custom/Export')
    print self.opener.open(url, data).read()
    report_data = self.opener.open(url, data).readlines()
    report_data = report_data[1:]  # Remove the first comment line.
    contributions = []
    reader = csv.DictReader(report_data)
    for row in reader:
      contributions.append(row)
    return contributions
