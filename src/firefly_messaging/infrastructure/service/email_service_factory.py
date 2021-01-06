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

import firefly_di as di
import firefly as ff

import firefly_messaging.domain as domain
from firefly_messaging.domain import EmailService


class EmailServiceFactory(domain.EmailServiceFactory):
    _container: di.Container = None

    def __call__(self, service: str = None) -> EmailService:
        if service is None:
            return self._container.email_service

        try:
            return getattr(self._container, f'{service}_email_service')
        except AttributeError:
            raise ff.ConfigurationError(f'No service registered for {service}')
