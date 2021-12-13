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
import re

from ... import domain as domain
from .aws_ses_client_factory import AwsSESClientFactory


class AwsSESEmailService(domain.EmailService):
    _client_factory: AwsSESClientFactory = None
    _email_regex: str = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    def add_contact_to_audience(self, contact: domain.Contact, audience: domain.Audience, meta: dict = None,
                                tags: list = None):
        raise NotImplementedError()

    def add_tag_to_audience_member(self, tag: str, audience: domain.Audience, contact: domain.Contact):
        raise NotImplementedError()

    def remove_tag_from_audience_member(self, tag: str, audience: domain.Audience, contact: domain.Contact):
        raise NotImplementedError()

    def send_email(self, subject: str, text_body: str, html_body: str, from_address: str, to_address: List[str], cc_addresses: List[str], bcc_addresses: List[str]):
        if isinstance(to_address, str):
            if re.match(self._email_regex, to_address):
                to_address = [to_address]
            else:
                raise Exception('Invalid Destination address')
        client = self._get_client()
        response = client.send_email(
            Source=from_address,
            Destination={
                'ToAddresses': to_address,
                'CcAddresses': cc_addresses,
                'BccAddresses': bcc_addresses,
            },
            Message={
                'Subject': {
                    'Data': subject,
                },
                'Body': {
                    'Text': {
                        'Data': text_body,
                    },
                    'Html': {
                        'Data': html_body,
                    }
                }
            }
        )
        return response

    def _get_client(self):
        return self._client_factory()
