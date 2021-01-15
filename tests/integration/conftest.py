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


@pytest.fixture(scope='session')
def config():
    return {
        'contexts': {
            'firefly_messaging': {
                'is_extension': True,
            },
            'messaging': {
                'extends': 'firefly_messaging',
                'storage': {
                    'services': {
                        'rdb': {
                            'connection': {
                                'driver': 'sqlite',
                                'host': ':memory:'
                                # 'host': '/tmp/todo.db'
                            }
                        },
                    },
                    'default': 'rdb',
                },
            },
        },
    }


@pytest.fixture()
def tenant(registry):
    tenants = registry(domain.Tenant)
    tenant = domain.Tenant(name='Firefly')
    tenants.append(tenant)
    tenants.commit()
    return tenant


@pytest.fixture()
def audience(registry, tenant):
    audiences = registry(domain.Audience)
    audience = domain.Audience(
        name='My Audience',
        tenant=tenant,
        meta={
            'mc_api_key': 'abc123',
            'mc_id': 'abc123',
        },
    )
    audiences.append(audience)
    audiences.commit()
    return audience


@pytest.fixture(autouse=True)
def audience_member(registry, audience, contact):
    audience_members = registry(domain.AudienceMember)
    audience_member = domain.AudienceMember(
        audience=audience.id,
        contact=contact.id,
        meta={'mc_id': 'abc123'},
    )
    audience_members.append(audience_member)
    audience_members.commit()
    audience_members.reset()
    return audience_member


@pytest.fixture()
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
