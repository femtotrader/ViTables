#       Copyright (C) 2005-2007 Carabos Coop. V. All rights reserved
#       Copyright (C) 2008-2024 Vicent Mas. All rights reserved
#
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#       Author:  Vicent Mas - vmas@vitables.org

"""This is the launcher script for the ViTables application."""

import argparse
import atexit
import locale
import logging
import os.path
import sys
import traceback

from qtpy import QtCore, QtWidgets

from vitables.preferences import vtconfig
from vitables.vtapp import VTApp

__docformat__ = 'restructuredtext'

# Map number of -v's on command line to logging error level.
_VERBOSITY_LOGLEVEL_DICT = {0: logging.ERROR, 1: logging.WARNING,
                            2: logging.INFO, 3: logging.DEBUG}
# Default log format used by logger.
_FILE_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# Folder with vitables translations.
_I18N_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'i18n')


_uncaught_exception_logger = logging.getLogger('uncaught_logger')


def _uncaught_exception_hook(type_, value, tb):
    _uncaught_exception_logger.error(''.join(traceback.format_tb(tb))
                                     + str(value))
    sys.__excepthook__(type_, value, tb)


sys.excepthook = _uncaught_exception_hook


def _check_versions():
    """Check that tables are at least version 3.0"""
    import tables
    if tables.__version__ < '3.0':
        sys.exit('FATAL: PyTables version 3.0 or above is required, '
                 f'installed version is {tables.__version__}')


def _set_credentials(app):
    """Specify the organization's Internet domain.

    When the Internet domain is set, it is used on Mac OS X instead of
    the organization name, since Mac OS X applications conventionally
    use Internet domains to identify themselves

    """
    app.setOrganizationDomain('vitables.org')
    app.setOrganizationName('ViTables')
    app.setApplicationName('ViTables')
    app.setApplicationVersion(vtconfig.getVersion())


def _set_locale(app):
    """Set locale and load translation if available.

    Localize the application using the system locale numpy seems to
    have problems with decimal separator in some locales (catalan,
    german...) so C locale is always used for numbers.

    """
    locale.setlocale(locale.LC_ALL, '')
    locale.setlocale(locale.LC_NUMERIC, 'C')

    locale_name = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    if translator.load('vitables_' + locale_name, _I18N_PATH):
        app.installTranslator(translator)
    return translator


def _parse_command_line():
    """Create parser and parse command line."""
    # Parse the command line optional arguments
    parser = argparse.ArgumentParser(usage='%(prog)s [option]... [h5file]...')
    h5files_group = parser.add_argument_group('h5files')
    logging_group = parser.add_argument_group('logging')
    # Options for the default group
    parser.add_argument(
        '--version', action='version',
        version=f'%(prog)s {vtconfig.getVersion()}')
    # Options for opening files
    h5files_group.add_argument(
        '-m', '--mode', choices=['r', 'a'], metavar='MODE',
        help='mode access for a database. Can be r(ead) or a(ppend)')
    h5files_group.add_argument('-d', '--dblist',
                               help=('a file with the list of HDF5 '
                                     'filepaths to be open'))
    # Logging options
    logging_group.add_argument('-l', '--log-file', help='log file path')
    logging_group.add_argument('-v', '--verbose', action='count', default=0,
                               help='log verbosity level')
    # Allow an optional list of input filepaths
    parser.add_argument('h5file', nargs='*')
    # Set sensible option defaults
    parser.set_defaults(mode='a', dblist='', h5file=[])
    # parse and process arguments
    args = parser.parse_args()
    if args.dblist:
        # Other options and positional arguments are silently ignored
        args.mode = ''
        args.h5file = []
    return args


def _setup_logger(args):
    """Setup root logger output format, level and output file.

    Stderr logger is added to handle error that raise before the gui
    is launched. It better be removed before event loop starts.

    """
    logger = logging.getLogger()
    file_formatter = logging.Formatter(_FILE_LOG_FORMAT)
    temporary_stderr_handler = logging.StreamHandler()
    temporary_stderr_handler.setFormatter(file_formatter)
    logger.addHandler(temporary_stderr_handler)
    if args.log_file is not None:
        try:
            log_filename = os.path.expandvars(
                os.path.expanduser(args.log_file))
            file_handler = logging.FileHandler(log_filename)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error('Failed to open log file')
            logger.error(e)
    if args.verbose in _VERBOSITY_LOGLEVEL_DICT:
        logger.setLevel(_VERBOSITY_LOGLEVEL_DICT[args.verbose])
    else:
        logger.setLevel(logging.ERROR)
        logger.error(f'Invalid verbosity level: {args.verbose}, error level '
                     'set to ERROR')
    return logger, temporary_stderr_handler


def _close_open_files(verbose=None):
    """Close all open files in the current HDF5 library.

    This cleanup function is useful to avoid UnclosedFileWarning messages when
    ViTables quits. It is called by the atexit module.

    """

    import tables

    open_files = tables.file._open_files

    are_open_files = len(open_files) > 0

    if verbose and are_open_files:
        sys.stderr.write("Closing remaining open files:")

    if tables.__version__ >= "3.1.0":
        # make a copy of the open_files.handlers container for the iteration
        handlers = list(open_files.handlers)
    else:
        # for older versions of pytables, setup the handlers list from the
        # keys
        keys = open_files.keys()
        handlers = []
        for key in keys:
            handlers.append(open_files[key])

    for fileh in handlers:
        if verbose:
            sys.stderr.write(f"{fileh.filename}...")

        fileh.close()

        if verbose:
            sys.stderr.write("done")

    if verbose and are_open_files:
        sys.stderr.write("\n")


def gui():
    """The application launcher.

    First of all, translators are loaded. Then the GUI is shown and
    the events loop is started.

    """
    _check_versions()
    app = QtWidgets.QApplication(sys.argv)
    _set_credentials(app)
    translator = _set_locale(app)  # must not be destroyed before app quits
    args = _parse_command_line()
    root_logger, console_log_handler = _setup_logger(args)
    vtapp = VTApp(mode=args.mode, dblist=args.dblist, h5files=args.h5file)
    vtapp.gui.show()
    root_logger.removeHandler(console_log_handler)
    app.exec_()


if __name__ == '__main__':
    atexit.register(_close_open_files, False)
    gui()
