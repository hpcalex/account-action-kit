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

# Check existence of group
if ! getent group "$project"; then
  >&2 echo "ERROR: Group $project does not exist in the system"
  exit 1
fi

# Check scheduler for project
if [ "$(sacctmgr -np show account "$project")" ]; then
  >&2 echo "ERROR: Project $project is already defined"
  exit 1
fi

cpu_hours="$core_hours"  # To be renamed in fields in the future

# In Slurm commands, --cluster is also -M, --partition is also -p
M=c2

for p in cpu gpu; do
  defined=

  if [ "$p" = cpu ] && [ "$cpu_hours" -ne 0 ]; then
    defined=1
    acct_desig=
    key=cpu
    val=$((cpu_hours*60))
  fi

  if [ "$p" = gpu ] && [ "$gpu_hours" -ne 0 ]; then
    defined=1
    acct_desig=g.
    key=gres/gpu
    val=$((gpu_hours*60))
  fi

  if [ ! "$defined" ]; then
    continue
  fi

  sacctmgr -i add account "$acct_desig$project" cluster="$M" grptresmins+="$key=$val"
  sed -i "/^\<PartitionName=$p\>/s/\<AllowAccounts=[^ ]\+\>/&,$acct_desig$project/" /etc/slurm/parts
done

rocks sync slurm
