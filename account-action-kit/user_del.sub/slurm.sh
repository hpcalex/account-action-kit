#!/bin/sh
set -e

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

M=c2

accts=$(sacctmgr -np list accounts | \
  cut -d\| -f2 | egrep "(^|\\.)$project\$" | tr \\n , | sed 's/,$//')
echo "$accts"

# Accounts would have to be sorted with default account last otherwise
sacctmgr -i remove user "$user" account="$accts" cluster="$M"
