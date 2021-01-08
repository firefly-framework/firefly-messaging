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

    member = audience.get_member_by_contact(contact)
    assert member.contact.id == contact.id


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

    member = audience.get_member_by_contact(contact)

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

    member = audience.get_member_by_contact(contact)

    assert 'foo' not in member.tags


@pytest.fixture(scope='function')
def tenant(registry):
    tenants = registry(domain.Tenant)
    tenant = domain.Tenant(name='Firefly')
    tenants.append(tenant)
    tenants.commit()
    return tenant


@pytest.fixture(scope='function')
def audience(registry, tenant):
    audiences = registry(domain.Audience)
    audience = domain.Audience(
        name='My Audience',
        tenant=tenant,
    )
    audiences.append(audience)
    audiences.commit()
    return audience


@pytest.fixture(scope='function')
def contact(registry):
    contacts = registry(domain.Contact)
    contact = domain.Contact(
        email='foo@bar.com',
        given_name='Bob',
        family_name='Loblaw',
        birthdate=datetime(year=1990, month=1, day=1)
    )
    contacts.append(contact)
    contacts.commit()
    return contact
