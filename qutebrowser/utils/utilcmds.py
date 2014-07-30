# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2014 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Misc. utility commands exposed to the user."""

from functools import partial

import qutebrowser.commands.utils as cmdutils
from qutebrowser.utils.usertypes import Timer
from qutebrowser.commands.exceptions import CommandError
from qutebrowser.commands.managers import CommandManager


_timers = []
_commandmanager = None


def init():
    """Initialize the global _commandmanager."""
    global _commandmanager
    _commandmanager = CommandManager()


@cmdutils.register(nargs=(2, None))
def later(ms, *command):
    """Execute a command after some time.

    Args:
        ms: How many milliseconds to wait.
        command: The command/args to run.
    """
    ms = int(ms)
    timer = Timer(name='later')
    timer.setSingleShot(True)
    if ms < 0:
        raise CommandError("I can't run something in the past!")
    try:
        timer.setInterval(ms)
    except OverflowError:
        raise CommandError("Numeric argument is too large for internal int "
                           "representation.")
    _timers.append(timer)
    cmdline = ' '.join(command)
    timer.timeout.connect(partial(_commandmanager.run_safely, cmdline))
    timer.timeout.connect(lambda: _timers.remove(timer))
    timer.start()