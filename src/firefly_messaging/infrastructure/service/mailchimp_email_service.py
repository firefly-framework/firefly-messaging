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

from mailchimp3 import MailChimp

from ... import domain as domain


class MailchimpEmailService(domain.EmailService):
    def add_contact_to_audience(self, contact: domain.Contact, audience: domain.Audience):
        client = self._get_client(audience)
        member = client.lists.members.create(audience.meta['mc_id'], {
            'email_address': contact.email,
            'status': 'subscribed',
        })
        contact.meta['mc_id'] = member['id']

    def add_tag_to_audience_member(self, tag: str, audience: domain.Audience, contact: domain.Contact):
        client = self._get_client(audience)
        client.lists.members.tags.update(
            audience.meta['mc_id'],
            audience.get_member_by_contact(contact).meta['mc_id'],
            {'tags': [{'name': tag, 'status': 'active'}]}
        )

    def remove_tag_from_audience_member(self, tag: str, audience: domain.Audience, contact: domain.Contact):
        client = self._get_client(audience)
        client.lists.members.tags.update(
            audience.meta['mc_id'],
            audience.get_member_by_contact(contact).meta['mc_id'],
            {'tags': [{'name': tag, 'status': 'inactive'}]}
        )

    @staticmethod
    def _get_client(audience: domain.Audience):
        return MailChimp(mc_api=audience.meta['mc_api_key'])
