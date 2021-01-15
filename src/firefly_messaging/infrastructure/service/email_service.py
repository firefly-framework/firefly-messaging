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

import firefly as ff

import firefly_messaging.domain as domain


class EmailService(domain.EmailService):
    _registry: ff.Registry = None
    _email_service_factory: domain.EmailServiceFactory = None

    def add_contact_to_audience(self, contact: domain.Contact, audience: domain.Audience, meta: dict = None,
                                tags: list = None):
        audience_members = self._registry(domain.AudienceMember)
        audience_member = self._get_audience_member(audience, contact)
        if audience_member is not None:
            audience_member.meta.update(meta or {})
            audience_member.tags.extend(tags or [])
        else:
            audience_members.append(domain.AudienceMember(
                audience=audience.id,
                contact=contact.id,
                meta=meta or {},
                tags=tags or []
            ))

        for service in audience.services:
            self._email_service_factory(service).add_contact_to_audience(contact, audience, meta, tags)

    def add_tag_to_audience_member(self, tag: str, audience: domain.Audience, contact: domain.Contact):
        audience_member = self._get_audience_member(audience, contact)
        if audience_member is None or tag in audience_member.tags:
            return

        audience_member.tags.append(tag)
        for service in audience.services:
            self._email_service_factory(service).add_tag_to_audience_member(tag, audience, contact)

    def remove_tag_from_audience_member(self, tag: str, audience: domain.Audience, contact: domain.Contact):
        audience_member = self._get_audience_member(audience, contact)
        if audience_member is None or tag not in audience_member.tags:
            return

        audience_member.tags.remove(tag)
        for service in audience.services:
            self._email_service_factory(service).remove_tag_from_audience_member(tag, audience, contact)

    def _get_audience_member(self, audience: domain.Audience, contact: domain.Contact):
        return self._registry(domain.AudienceMember).find(
            lambda am: (am.audience == audience.id) & (am.contact == contact.id)
        )
