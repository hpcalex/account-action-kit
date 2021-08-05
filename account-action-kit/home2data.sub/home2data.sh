#!/bin/bash
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

usage () {
  >&2 echo "Usage: $0"
}

if [ "$#" -ne 0 ]; then
  usage
  exit 1
fi

cd "$HOME"

for i in cache/pip cache/torch conda/pkgs conda/envs local/bin local/lib; do
  # Assume a single slash
  dst="data/${i/\//_}"

  if [ ! -e "./$dst" ]; then
    if [ -e ".$i" ]; then
      echo "Linking .$i... (moving)" >&2
      mv ".$i" "./$dst"
    else
      echo "Linking .$i..." >&2
    fi

    mkdir -p "$(dirname ".$i")" "./$dst"
    ln -s "../$dst" ".$i"
  fi
done
