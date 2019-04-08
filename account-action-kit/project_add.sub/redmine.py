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


def get_support_group(redmine):
    for grp in redmine.group.all():
        if grp.name == 'support':
            return grp


def get_issue_tracker(redmine):
    for tracker in redmine.tracker.all():
        if tracker.name == 'issue':
            return tracker


def add_project(project_name, redmine):
    support_group = get_support_group(redmine=redmine)

    if support_group is None:
        exit("Couldn't find Redmine support group")

    issue_tracker = get_issue_tracker(redmine=redmine)

    if issue_tracker is None:
        exit("Couldn't find Redmine issue tracker")

    project = redmine.project.new()
    project.name = project_name
    project.identifier = project_name
    project.is_public = False
    project.tracker_ids = [issue_tracker.id]
    project.enabled_module_names = ['issue_tracking', 'time_tracking']

    try:
        project.save()
    except exceptions.ValidationError as e:
        exit('Error adding Redmine project \'%s\': %s' % (project.name, e.message))

    membership = redmine.project_membership.new()
    membership.project_id = project.id
    membership.user_id = support_group.id
    membership.role_ids = [4]

    try:
        membership.save()
    except exceptions.ValidationError as e:
        exit('Error adding support group to Redmine project \'%s\': %s' % (project.name, e.message))


def main():
    parser = argparse.ArgumentParser(usage='', add_help=False)

    parser.add_argument('--project')
    parser.add_argument('--redmine-url')
    parser.add_argument('--redmine-key-file')

    parser.add_argument('--help', action='store_true', default=False)

    args = vars(parser.parse_args())

    if args['project'] is None or args['redmine_url'] is None or args['redmine_key_file'] is None:
        exit('Invalid usage')

    try:
        redmine_key_file = open(args['redmine_key_file'], 'r')
        redmine_key = redmine_key_file.read().strip('\r\n')
    except IOError as e:
        exit('Error reading Redmine API key file \'%s\': %s' % (args['redmine_key_file'], e.strerror))

    redmine = Redmine(args['redmine_url'], key=redmine_key, requests={'verify': False})
    add_project(project_name=args['project'], redmine=redmine)


if __name__ == '__main__':
    main()

# vim: ts=4: sts=4: sw=4:
