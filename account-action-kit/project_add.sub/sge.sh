#!/bin/sh
set -e

# Copyright (C) 2016-2019 Bibliotheca Alexandrina
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

accounting_prefix=/share/accounting
cores=400

# Check existence of group
if ! getent group "$project"; then
  >&2 echo "ERROR: Group $project does not exist in the system"
  exit 1
fi

# Check scheduler for department
if ! qconf -su "$dept"; then
  >&2 echo "ERROR: Department $dept is not defined"
  exit 1
fi

# Check scheduler for project
if qconf -su "$project"; then
  >&2 echo "ERROR: Project $project is already defined"
  exit 1
fi

# Add project
input_file=$(mktemp)
cat <<EOF > "$input_file"
name $project
type ACL
fshare 0
oticket 0
entries NONE
EOF
qconf -Au \
  "$input_file" > /dev/null 2>&1 && rm "$input_file"

input_file=$(mktemp)
cat <<EOF > "$input_file"
name $project
oticket 0
fshare 0
acl $project
xacl NONE
EOF
qconf -Aprj \
  "$input_file" > /dev/null 2>&1 && rm "$input_file"

qconf -aattr queue projects "$project" all.q > /dev/null 2>&1

core_seconds=$(($core_hours * 3600))
echo ";;$project;;;$core_seconds" > "$accounting_prefix/$project"
chown sge:sge "$accounting_prefix/$project"

input_file=$(mktemp)
cat <<EOF > "$input_file"
{
  name $project
  description NONE
  enabled TRUE
  limit projects $project to slots=$cores
}
EOF
qconf -drqs "$project" > /dev/null 2>&1
qconf -Arqs \
  "$input_file" > /dev/null 2>&1 && rm "$input_file"

input_file=$(mktemp)
qconf -srqs "$dept" | sed "s/projects /projects $project,/" > "$input_file"
qconf -drqs "$dept" > /dev/null 2>&1
qconf -Arqs \
  "$input_file" > /dev/null 2>&1 && rm "$input_file"
