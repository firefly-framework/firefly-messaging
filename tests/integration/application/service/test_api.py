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

from datetime import datetime

import pytest

import firefly_messaging.domain as domain


def test_add_contact_to_audience(system_bus, audience, contact, registry):
    system_bus.invoke('messaging.AddContactToAudience', {
        'contact_id': contact.id,
        'audience_id': audience.id,
    })

    audience: domain.Audience = registry(domain.Audience)[0]
    contact: domain.Contact = registry(domain.Contact)[0]

    member = registry(domain.AudienceMember).find(lambda am: (am.audience == audience.id) & (am.contact == contact.id))
    assert member.contact == contact.id


def test_add_contact_to_audience_with_meta(system_bus, audience, contact, registry):
    system_bus.invoke('messaging.AddContactToAudience', {
        'contact_id': contact.id,
        'audience_id': audience.id,
        'meta': {
            'my_key': 'my_value'
        }
    })

    audience: domain.Audience = registry(domain.Audience)[0]
    contact: domain.Contact = registry(domain.Contact)[0]

    member = registry(domain.AudienceMember).find(lambda am: (am.audience == audience.id) & (am.contact == contact.id))
    assert member.meta['my_key'] == 'my_value'


def test_add_contact_to_audience_with_tags(system_bus, audience, contact, registry):
    system_bus.invoke('messaging.AddContactToAudience', {
        'contact_id': contact.id,
        'audience_id': audience.id,
        'tags': ['my_tag']
    })

    audience: domain.Audience = registry(domain.Audience)[0]
    contact: domain.Contact = registry(domain.Contact)[0]

    member = registry(domain.AudienceMember).find(lambda am: (am.audience == audience.id) & (am.contact == contact.id))
    assert 'my_tag' in member.tags


def test_add_tag_to_audience_member(system_bus, audience, contact, registry):
    system_bus.invoke('messaging.AddContactToAudience', {
        'contact_id': contact.id,
        'audience_id': audience.id,
    })

    system_bus.invoke('messaging.AddTagToAudienceMember', {
        'tag': 'foo',
        'contact_id': contact.id,
        'audience_id': audience.id,
    })

    audience: domain.Audience = registry(domain.Audience)[0]
    contact: domain.Contact = registry(domain.Contact)[0]

    member = registry(domain.AudienceMember).find(lambda am: (am.audience == audience.id) & (am.contact == contact.id))

    assert 'foo' in member.tags


def test_remove_tag_from_audience_member(system_bus, audience, contact, registry):
    system_bus.invoke('messaging.AddContactToAudience', {
        'contact_id': contact.id,
        'audience_id': audience.id,
    })

    system_bus.invoke('messaging.AddTagToAudienceMember', {
        'tag': 'foo',
        'contact_id': contact.id,
        'audience_id': audience.id,
    })

    system_bus.invoke('messaging.RemoveTagFromAudienceMember', {
        'tag': 'foo',
        'contact_id': contact.id,
        'audience_id': audience.id,
    })

    audience: domain.Audience = registry(domain.Audience)[0]
    contact: domain.Contact = registry(domain.Contact)[0]

    member = registry(domain.AudienceMember).find(lambda am: (am.audience == audience.id) & (am.contact == contact.id))

    assert 'foo' not in member.tags
