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

from abc import ABC, abstractmethod

import firefly_messaging.domain as domain


class EmailService(ABC):
    @abstractmethod
    def add_contact_to_audience(self, contact: domain.Contact, audience: domain.Audience, meta: dict = None,
                                tags: list = None):
        pass

    @abstractmethod
    def add_tag_to_audience_member(self, tag: str, audience: domain.Audience, contact: domain.Contact):
        pass

    @abstractmethod
    def remove_tag_from_audience_member(self, tag: str, audience: domain.Audience, contact: domain.Contact):
        pass
