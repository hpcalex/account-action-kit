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

# Quota is soft limit, limit is hard limit
lfs_blimitg="$lfs_bquotag"
lfs_ilimitg="$lfs_iquotag"
lfs setquota -g "$project" -b "$lfs_bquotag"G -B "$lfs_blimitg"G -i "$lfs_iquotag" -I "$lfs_ilimitg" "$(df --output=target "$lfs_prefix" | tail -n 1)"
