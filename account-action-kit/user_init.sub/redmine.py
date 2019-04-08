#!/usr/bin/env python

# Copyright (C) 2017-2019 Bibliotheca Alexandrina
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import string
import random
import argparse
from redmine import Redmine, exceptions


def init_user(email, redmine):
    found = False
    for user in redmine.user.all():
        if user.mail == email:
            found = True
            break

    if not found:
        exit('Couldn\'t find Redmine user with email \'%s\'' % email)

    pw_domain = string.ascii_letters + string.digits + string.punctuation
    random.shuffle(list(pw_domain))
    pw = ''.join(random.sample(pw_domain, 12))

    user.password = pw
    user.send_information = 1

    try:
        user.save()
    except exceptions.ValidationError as e:
        exit('Error setting password for Redmine user \'%s\': %s' % (user.login, e.message))


def main():
    parser = argparse.ArgumentParser(usage='', add_help=False)

    parser.add_argument('--email')
    parser.add_argument('--redmine-url')
    parser.add_argument('--redmine-key-file')

    parser.add_argument('--help', action='store_true', default=False)

    args = vars(parser.parse_args())

    if args['email'] is None or args['redmine_url'] is None or args['redmine_key_file'] is None:
        exit('Invalid usage')

    try:
        redmine_key_file = open(args['redmine_key_file'], 'r')
        redmine_key = redmine_key_file.read().strip('\r\n')
    except IOError as e:
        exit('Error reading Redmine API key file \'%s\': %s' % (args['redmine_key_file'], e.strerror))

    redmine = Redmine(args['redmine_url'], key=redmine_key, requests={'verify': False})
    init_user(email=args['email'], redmine=redmine)


if __name__ == '__main__':
    main()

# vim: ts=4: sts=4: sw=4:
