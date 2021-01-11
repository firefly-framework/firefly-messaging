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

from unittest.mock import MagicMock, call

import pytest

import firefly_messaging.infrastructure as infra
from firefly_messaging.application.container import Container


def test_add_contact_to_audience_basic(sut, mailchimp_client, audience, contact):
    mailchimp_client.lists.members.create.return_value = {'id': 'abc123'}
    sut.add_contact_to_audience(contact, audience)

    mailchimp_client.lists.members.create.assert_called_with(
        audience.meta['mc_id'],
        {
            'email_address': contact.email,
            'status': 'subscribed',
        },
    )
    assert audience.get_member_by_contact(contact).meta['mc_id'] == 'abc123'


def test_add_contact_to_audience_with_tags(sut, mailchimp_client, audience, contact):
    mailchimp_client.lists.members.create.return_value = {'id': 'abc123'}
    sut.add_contact_to_audience(contact, audience, tags=['tag1', 'tag2'])

    mailchimp_client.lists.members.create.assert_called_with(
        audience.meta['mc_id'],
        {
            'email_address': contact.email,
            'status': 'subscribed',
            'tags': ['tag1', 'tag2']
        },
    )
    assert audience.get_member_by_contact(contact).meta['mc_id'] == 'abc123'


def test_add_contact_to_audience_with_existing_merge_fields(sut, mailchimp_client, audience, contact):
    mailchimp_client.lists.members.create.return_value = {'id': 'abc123'}
    mailchimp_client.lists.merge_fields.all.return_value = {
        'merge_fields': [
            {'name': 'First Name', 'tag': 'FNAME'},
            {'name': 'Last Name', 'tag': 'LNAME'},
        ],
    }
    sut.add_contact_to_audience(contact, audience, meta={'First Name': 'Bob', 'Last Name': 'Loblaw'})

    mailchimp_client.lists.members.create.assert_called_with(
        audience.meta['mc_id'],
        {
            'email_address': contact.email,
            'status': 'subscribed',
            'merge_fields': {
                'FNAME': 'Bob',
                'LNAME': 'Loblaw'
            },
            'skip_merge_validation': True,
        },
    )


def test_add_contact_to_audience_with_extra_merge_fields(sut, mailchimp_client, audience, contact):
    mailchimp_client.lists.members.create.return_value = {'id': 'abc123'}
    mailchimp_client.lists.merge_fields.all.return_value = {
        'merge_fields': [
            {'name': 'First Name', 'tag': 'FNAME'},
            {'name': 'Last Name', 'tag': 'LNAME'},
            {'name': 'Address', 'tag': 'MERGE1'},
        ]
    }
    sut.add_contact_to_audience(contact, audience, meta={'First Name': 'Bob', 'Last Name': 'Loblaw'})

    mailchimp_client.lists.members.create.assert_called_with(
        audience.meta['mc_id'],
        {
            'email_address': contact.email,
            'status': 'subscribed',
            'merge_fields': {
                'FNAME': 'Bob',
                'LNAME': 'Loblaw'
            },
            'skip_merge_validation': True,
        },
    )


def test_add_contact_to_audience_with_non_existent_merge_fields(sut, mailchimp_client, audience, contact):
    mailchimp_client.lists.members.create.return_value = {'id': 'abc123'}
    mailchimp_client.lists.merge_fields.all.return_value = {
        'merge_fields': [
            {'name': 'First Name', 'tag': 'FNAME'},
            {'name': 'Last Name', 'tag': 'LNAME'},
        ]
    }
    mailchimp_client.lists.merge_fields.create.side_effect = [
        {'tag': 'MERGE5'},
        {'tag': 'MERGE6'},
        {'tag': 'MERGE7'},
        {'tag': 'MERGE8'},
        {'tag': 'MERGE9'},
    ]
    sut.add_contact_to_audience(
        contact, audience, meta={
            'First Name': 'Bob',
            'Last Name': 'Loblaw',
            'customField': 'foobar',
            'customDate': '2021-01-01T00:00:00',
            'birthdate': '2021-01-01T00:00:00',
            'customFloat': 10.1,
            'customInt': 10,
        }
    )

    mailchimp_client.lists.members.create.assert_called_with(
        audience.meta['mc_id'],
        {
            'email_address': contact.email,
            'status': 'subscribed',
            'merge_fields': {
                'FNAME': 'Bob',
                'LNAME': 'Loblaw',
                'MERGE5': 'foobar',
                'MERGE6': '2021-01-01T00:00:00',
                'MERGE7': '2021-01-01T00:00:00',
                'MERGE8': 10.1,
                'MERGE9': 10,
            },
            'skip_merge_validation': True,
        },
    )

    mailchimp_client.lists.merge_fields.create.assert_has_calls(
        [
            call(
                audience.meta['mc_id'],
                {
                    'default_value': '',
                    'help_text': '',
                    'name': 'customField',
                    'public': True,
                    'required': False,
                    'type': 'text'
                }
            ),
            call(
                audience.meta['mc_id'],
                {
                    'default_value': '',
                    'help_text': '',
                    'name': 'customDate',
                    'public': True,
                    'required': False,
                    'type': 'date'
                }
            ),
            call(
                audience.meta['mc_id'],
                {
                    'default_value': '',
                    'help_text': '',
                    'name': 'birthdate',
                    'public': True,
                    'required': False,
                    'type': 'date'
                }
            ),
            call(
                audience.meta['mc_id'],
                {
                    'default_value': '',
                    'help_text': '',
                    'name': 'customFloat',
                    'public': True,
                    'required': False,
                    'type': 'number'
                }
            ),
            call(
                audience.meta['mc_id'],
                {
                    'default_value': '',
                    'help_text': '',
                    'name': 'customInt',
                    'public': True,
                    'required': False,
                    'type': 'number'
                }
            ),
        ]
    )


def test_add_tag_to_audience_member(sut, mailchimp_client, audience, contact):
    sut.add_tag_to_audience_member('my_tag', audience, contact)

    mailchimp_client.lists.members.tags.update.assert_called_with(
        audience.meta['mc_id'],
        audience.get_member_by_contact(contact).meta['mc_id'],
        {'tags': [{'name': 'my_tag', 'status': 'active'}]}
    )


def test_remove_tag_from_audience_member(sut, mailchimp_client, audience, contact):
    sut.remove_tag_from_audience_member('my_tag', audience, contact)

    mailchimp_client.lists.members.tags.update.assert_called_with(
        audience.meta['mc_id'],
        audience.get_member_by_contact(contact).meta['mc_id'],
        {'tags': [{'name': 'my_tag', 'status': 'inactive'}]}
    )


@pytest.fixture()
def sut(mailchimp_client):
    class Sut(infra.MailchimpEmailService):
        pass
    ret = Container().mock(Sut)
    ret._client_factory.return_value = mailchimp_client
    return ret


@pytest.fixture()
def mailchimp_client():
    return MagicMock()
