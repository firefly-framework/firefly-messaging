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

from typing import List, Optional

import firefly as ff

import firefly_messaging.domain as domain

MAILCHIMP = 'mailchimp'


class Audience(ff.AggregateRoot):
    id: str = ff.id_()
    name: str = ff.required()
    tenant: domain.Tenant = ff.required()
    members: List[domain.AudienceMember] = ff.list_()
    campaigns: List[domain.Campaign] = ff.list_()
    services: list = ff.list_(validators=ff.IsOneOf((MAILCHIMP,)))
    meta: dict = ff.dict_()

    def get_member_by_contact(self, contact: domain.Contact) -> Optional[domain.AudienceMember]:
        for member in self.members:
            if member.contact.id == contact.id:
                return member

    def get_campaign(self, id_: str) -> Optional[domain.Campaign]:
        for campaign in self.campaigns:
            if campaign.id == id_:
                return campaign

    def add_member(self, contact: domain.Contact, meta: dict = None, tags: list = None):
        if self.get_member_by_contact(contact) is None:
            self.members.append(
                domain.AudienceMember(
                    contact=contact,
                    meta=meta or {},
                    tags=tags or []
                )
            )
