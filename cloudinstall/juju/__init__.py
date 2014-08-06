#
# __init__.py - Juju state
#
# Copyright 2014 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Represents a juju status """

import logging

from cloudinstall.config import Config
from cloudinstall.machine import Machine
from cloudinstall.service import Service

log = logging.getLogger('cloudinstall.juju')


class JujuState:
    """ Represents a global Juju state """

    def __init__(self, juju):
        """ Builds a JujuState

        :param juju: Juju API connection
        """
        self.config = Config()
        self.juju = juju
        self.valid_states = ['pending', 'started', 'down']

    def machine(self, machine_id):
        """ Return single machine state

        :param str machine_id: machine machine_id
        :returns: machine
        :rtype: :class:`~cloudinstall.machine.Machine`
        """
        for m in self.machines():
            if m.machine_id == machine_id:
                return m
        return Machine(-1, {})

    def machines(self):
        """ Machines property

        :returns: machines known to juju (except bootstrap)
        :rtype: list
        """
        ret = self.juju.status()
        machines = []

        for machine_id, machine in ret.get('Machines', {}).items():
            if '0' == machine_id:
                continue
            machines.append(Machine(machine_id, machine))
        return machines

    def machines_allocated(self):
        """ Machines allocated property

        :returns: all machines in an allocated state (see self.valid_states)
        :rtype: list
        """
        return [m for m in self.machines()
                if m.agent_state in self.valid_states or
                m.agent['Status'] in self.valid_states]

    def service(self, name):
        """ Return a single service entry

        :param str name: service/charm name
        :returns: a service entry or None
        :rtype: :class:`~cloudinstall.service.Service`
        """
        for s in self.services:
            if s.service_name == name:
                return s
        return Service(name, {})

    @property
    def services(self):
        """ Juju services property

        :returns: Service() of all loaded services
        :rtype: list
        """
        ret = self.juju.status()
        services = []

        for name, service in ret.get('Services', {}).items():
            services.append(Service(name, service))

        return services

    @property
    def networks(self):
        """ Juju netwoks property
        """
        return self.juju.status()['Networks']
