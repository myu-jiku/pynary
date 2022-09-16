# Copyright 2022 Myu/Jiku
#
# This file is part of the Pynary package.
# Pynary is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# Pynary is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Pynary. If
# not, see <https://www.gnu.org/licenses/>

from pynary import PYNBlank

_pyn = PYNBlank()

_pyn.add_none()
_pyn.add_bool()
_pyn.add_int()
_pyn.add_float()
_pyn.add_str()
_pyn.add_list()
_pyn.add_tuple()
_pyn.add_set()
_pyn.add_dict()

dump: callable = _pyn.dump
load: callable = _pyn.load
