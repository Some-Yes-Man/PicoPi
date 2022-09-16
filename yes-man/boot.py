#!/usr/bin/python#
#  boot.py
#
#  Defines several useful functions to make using MicroPython on the Pi Pico
#  a little bit easier.
#
#  cat()             - Displays the a file, with optional line numbers.
#  create()          - Creates a file by reading from stdin, allowing a user
#                      to  create a new file simply by pasting its  contents
#                      into the console window.
#  ls()              - List the files in the current or specified folder.
#  rm()              - Deletes the specified file.
#  run()             - Executes a python script.
#  unload()          - Unloads a loaded module.
#
#  This  program is free software: you can redistribute it and/or modify  it
#  under  the  terms of the GNU General Public License as published  by  the
#  Free  Software  Foundation, either version 3 of the License, or (at  your
#  option) any later version.
#
#  This  program  is  distributed in the hope that it will  be  useful,  but
#  WITHOUT   ANY   WARRANTY;   without  even   the   implied   warranty   of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details.
#
#  You  should have received a copy of the GNU General Public License  along
#  with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  23 May 21   0.1   - Initial version - MT
#  24 May 21         - cat() now closes the input file - MT
#
#
#  To Do:
#
import sys
import os
import time


def create(_path):

    def _is_interrupt(_char):
        return _char in ('\x03')

    def _is_eof(_char):
        return _char in ('\x04', '\x1A')

    def _is_eoln(_char):
        return _char in ('\x0A', '\x0D')

    def _is_backspace(_char):
        return _char in ('\x08', '\x7F')

    def _getch():
        _char = ''
        while _char == '':
            _char = sys.stdin.read(1)
            if _is_interrupt(_char):
                raise KeyboardInterrupt
            elif _is_eof(_char):
                raise EOFError
            elif (_is_eoln(_char) or (31 <= ord(_char) < 127)):
                sys.stdout.write(_char)
            else:
                _char = ''
        return (_char)

    try:
        sys.stdout.write('\r')  # This seems to be important!
        for _module in sys.modules:
            if (sys.modules[_module].__file__ == _path):
                del sys.modules[_module]
        os.remove(_path)
    except OSError:
        pass
    except Exception as _error:
        sys.stderr.write(str(_error))
    finally:
        try:
            _file = open('' + _path + '', 'w')
            _count = 0
            _char = _getch()
            while not _is_eof(_char):
                _file.write(_char)
                if _is_eoln(_char):
                    _count += 1
                _char = _getch()
        except KeyboardInterrupt:
            _file.close()
            sys.exit(0)
        except EOFError:
            sys.stdout.write('\nWrote %d lines to \'%s\'' % (_count, _path))
        except Exception as _error:
            sys.stderr.write(str(_error))
        finally:
            sys.stdout.write('\n')
    _file.close()


def ls(path="."):
    try:
        _files = os.listdir(path)
        _files.sort()
        for _file in _files:
            _stat = os.stat("%s/%s" % (path, _file))
            if (_stat[0] & 0x4000):  # stat.S_IFDIR
                sys.stdout.write('   <dir> %s\n' % _file)
        for _file in _files:
            _stat = os.stat("%s/%s" % (path, _file))
            if not (_stat[0] & 0x4000):  # stat.S_IFDIR
                sys.stdout.write('% 8d %s\n' % (_stat[6], _file))
    except OSError as _error:
        sys.stderr.write('Path not found\n')
    except Exception as _error:
        sys.stderr.write(str(_error) + '\n')


def cat(_path, number=False):
    try:
        _count = 0
        with open(_path) as _file:
            if number:
                for _line in _file:
                    _count += 1
                    sys.stdout.write('%06d\t%s' % (_count, _line))
            else:
                sys.stdout.write(_file.read())
        _file.close()
    except OSError as _error:
        sys.stderr.write('File not found\n')
    except Exception as _error:
        sys.stderr.write(str(_error) + '\n')


def rm(_path):
    try:
        os.remove(_path)
    except OSError as _error:
        sys.stderr.write('File not found\n')
    except Exception as _error:
        sys.stderr.write(str(_error) + '\n')


def unload(_path):
    _count = 0
    for _module in sys.modules:
        if (sys.modules[_module].__file__ == _path):
            del sys.modules[_module]
            _count += 1
    if (_count == 0):
        sys.stderr.write('Module not loaded\n')


def run(_path):
    try:
        for _module in sys.modules:
            if (sys.modules[_module].__file__ == _path):
                del sys.modules[_module]
        _file = open(_path, 'r')
        _file.close()
    except OSError as _error:
        sys.stderr.write('File not found\n')
    except Exception as _error:
        sys.stderr.write(str(_error) + '\n')
    exec(open(_path).read())


time.sleep(2)
sys.stdout.write('Executing \'boot.py\'\n')
