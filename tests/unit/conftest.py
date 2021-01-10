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


@pytest.fixture(scope='function')
def tenant():
    return domain.Tenant(name='Firefly')


@pytest.fixture(scope='function')
def audience(tenant, contact):
    ret = domain.Audience(
        name='My Audience',
        tenant=tenant,
        meta={
            'mc_api_key': 'abc123',
            'mc_id': 'abc123',
        }
    )
    ret.add_member(contact, meta={'mc_id': 'abc123'})
    return ret


@pytest.fixture(scope='function')
def contact():
    return domain.Contact(
        email='foo@bar.com',
        given_name='Bob',
        family_name='Loblaw',
        birthdate=datetime(year=1990, month=1, day=1)
    )
