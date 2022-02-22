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
from firefly_messaging import domain
from firefly_messaging import infrastructure as infra


@ff.command_handler()
class AddContactToAudience(ff.ApplicationService):
    _registry: ff.Registry = None
    _email_service: domain.EmailService = None

    def __call__(self, contact_id: str, audience_id: str, meta: dict = None, tags: list = None, **kwargs):
        contact = self._registry(domain.Contact).find(contact_id)
        if contact is None:
            raise ff.NotFound('Contact not found')
        audience: domain.Audience = self._registry(domain.Audience).find(audience_id)
        if audience is None:
            raise ff.NotFound('Audience not found')

        self._email_service.add_contact_to_audience(contact, audience, meta, tags)


@ff.command_handler()
class AddTagToAudienceMember(ff.ApplicationService):
    _registry: ff.Registry = None
    _email_service: domain.EmailService = None

    def __call__(self, tag: str, audience_id: str, contact_id: str, **kwargs):
        contacts = self._registry(domain.Contact)
        contact = contacts.find(contact_id)
        if contact is None:
            self.info('No contact found for contact_id: %s', contact_id)
            raise ff.NotFound()

        audience: domain.Audience = self._registry(domain.Audience).find(audience_id)
        if audience is None:
            self.info('No audience found with id: %s', audience_id)
            raise ff.NotFound()

        self._email_service.add_tag_to_audience_member(tag, audience, contact)


@ff.command_handler()
class RemoveTagFromAudienceMember(ff.ApplicationService):
    _registry: ff.Registry = None
    _email_service: domain.EmailService = None

    def __call__(self, tag: str, audience_id: str, contact_id: str, **kwargs):
        contacts = self._registry(domain.Contact)
        contact = contacts.find(contact_id)
        if contact is None:
            self.info('No contact found for contact_id: %s', contact_id)
            raise ff.NotFound()

        audience: domain.Audience = self._registry(domain.Audience).find(audience_id)
        if audience is None:
            self.info('No audience found with id: %s', audience_id)
            raise ff.NotFound()

        self._email_service.remove_tag_from_audience_member(tag, audience, contact)

@ff.command_handler()
class SendSESEmail(ff.ApplicationService):
    _registry: ff.Registry = None
    _email_service: infra.AwsSESEmailService = None

    def __call__(self, subject: str, text_body: str, html_body: str, from_address: str, to_address: List[str], cc_addresses: List[str] = [], bcc_addresses: List[str] = [], **kwargs):
        resp = self._email_service.send_email(subject, text_body, html_body, from_address, to_address, cc_addresses, bcc_addresses)
        return resp
