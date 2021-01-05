#  Copyright (c) 2020 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.

from __future__ import annotations

from typing import List

import firefly as ff

import firefly_messaging.domain as domain


class Campaign(ff.Entity):
    id: str = ff.id_()
    name: str = ff.required()
    members: List[domain.AudienceMember] = ff.list_()

    def get_member_by_contact_id(self, contact_id: str):
        for member in self.members:
            if member.contact.id == contact_id:
                return member

    def add_contact(self, contact: domain.Contact, **kwargs):
        if self.get_member_by_contact_id(contact.id) is None:
            kwargs.update({'contact': contact})
            self.members.append(domain.AudienceMember(**ff.build_argument_list(kwargs, domain.AudienceMember)))
