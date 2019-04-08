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
import argparse
from redmine import Redmine, exceptions


def add_user(project_name, username, first_name, last_name, email, redmine):
    login = '%s.%s' % (first_name[0].lower(), last_name.lower())

    project = None
    try:
        project = redmine.project.get(project_name)
    except exceptions.ResourceNotFoundError as e:
        exit('Couldn\'t find Redmine project \'%s\': %s' % (project, e.message))

    found = False
    for role in redmine.role.all():
        if role.name == 'user':
            found = True
            break

    if not found:
        exit('Couldn\'t find Redmine user role')

    found = False
    for user in redmine.user.all():
        if user.mail == email:
            found = True
            break

    if not found:
        user = redmine.user.new()
        user.login = login
        user.firstname = first_name
        user.lastname = last_name
        user.mail = email
        user.mail_notification = 'only_my_events'
        user.must_change_passwd = True

        try:
            user.save()
        except exceptions.ValidationError as e:
            exit('Error adding Redmine user \'%s\': %s' % (user.login, e.__str__()))

    membership = redmine.project_membership.new()
    membership.project_id = project.id
    membership.user_id = user.id
    membership.role_ids = [user_role.id]

    try:
        membership.save()
    except exceptions.ValidationError as e:
        exit('Error adding Redmine user \'%s\' to project \'%s\': %s' % (user.login, project.name, e.__str__()))

    # Edit project description, mapping system user to Redmine login

    try:
        description = project.description
    except exceptions.ResourceAttrError:
        description = ''

    if len(description) > 0:
        description += '\n'

    description += '%s => %s' % (username, login)
    project.description = description

    try:
        project.save()
    except exceptions.ValidationError as e:
        exit('Error editing description for Redmine project \'%s\': %s' % (project.name, e.__str__()))


def main():
    parser = argparse.ArgumentParser(usage='', add_help=False)

    parser.add_argument('--project')
    parser.add_argument('--user')
    parser.add_argument('--first-name')
    parser.add_argument('--last-name')
    parser.add_argument('--email')
    parser.add_argument('--redmine-url')
    parser.add_argument('--redmine-key-file')

    parser.add_argument('--help', action='store_true', default=False)

    args = vars(parser.parse_args())

    if args['project'] is None or args['user'] is None or args['first_name'] is None or args['last_name'] is None or args['email'] is None or args['redmine_url'] is None or args['redmine_key_file'] is None:
        exit('Invalid usage')

    try:
        redmine_key_file = open(args['redmine_key_file'], 'r')
        redmine_key = redmine_key_file.read().strip('\r\n')
    except IOError as e:
        exit('Error reading Redmine API key file \'%s\': %s' % (args['redmine_key_file'], e.strerror))

    redmine = Redmine(args['redmine_url'], key=redmine_key, requests={'verify': False})
    add_user(project_name=args['project'], username=args['user'], first_name=args['first_name'], last_name=args['last_name'], email=args['email'], redmine=redmine)


if __name__ == '__main__':
    main()
