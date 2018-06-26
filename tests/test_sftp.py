# This file is part of ssh-python.
# Copyright (C) 2018 Panos Kittenis
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, version 2.1.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-130

import unittest
import os
import platform
import stat

from ssh.sftp import SFTP
from ssh.sftp_handles import SFTPDir, SFTPFile
from ssh.sftp_attributes import SFTPAttributes
from ssh.exceptions import InvalidAPIUse, SFTPHandleError

from .base_test import SSHTestCase


class SFTPTest(SSHTestCase):

    def test_sftp_init(self):
        self._auth()
        sftp = self.session.sftp_new()
        self.assertIsInstance(sftp, SFTP)
        self.assertEqual(sftp.init(), 0)

    def test_sftp_fail(self):
        self.assertRaises(InvalidAPIUse, self.session.sftp_new)
        self._auth()
        sftp = self.session.sftp_new()
        self.assertRaises(SFTPHandleError, sftp.opendir, '.')

    def test_sftp_dir(self):
        self._auth()
        sftp = self.session.sftp_new()
        sftp.init()
        _dir = sftp.opendir('.')
        self.assertIsInstance(_dir, SFTPDir)
        self.assertFalse(_dir.eof())
        self.assertEqual(_dir.closedir(), 0)
        # dir handle from context manager
        with sftp.opendir('.') as _dir:
            for attr in _dir:
                self.assertIsInstance(attr, SFTPAttributes)
                self.assertIsNotNone(attr.name)
        self.assertTrue(_dir.eof())

    def test_sftp_readdir(self):
        self._auth()
        sftp = self.session.sftp_new()
        sftp.init()
        with sftp.opendir('.') as _dir:
            attrs = _dir.readdir()
            self.assertIsInstance(attrs, SFTPAttributes)
            self.assertIsNotNone(attrs.uid)
            self.assertIsNotNone(attrs.gid)
            self.assertIsNotNone(attrs.owner)
            self.assertIsNotNone(attrs.group)
            self.assertTrue(attrs.size > 0)
            self.assertEqual(attrs.name, b'.')
            self.assertTrue(len(attrs.longname) > 1)

    def test_sftp_file_read(self):
        self._auth()
        sftp = self.session.sftp_new()
        sftp.init()
        if int(platform.python_version_tuple()[0]) >= 3:
            test_file_data = b'test' + bytes(os.linesep, 'utf-8')
        else:
            test_file_data = b'test' + os.linesep
        remote_filename = os.sep.join([os.path.dirname(__file__),
                                       'remote_test_file'])
        with open(remote_filename, 'wb') as test_fh:
            test_fh.write(test_file_data)
        try:
            with sftp.open(remote_filename, os.O_RDONLY, 0) as remote_fh:
                self.assertIsInstance(remote_fh, SFTPFile)
                remote_data = b""
                for rc, data in remote_fh:
                    remote_data += data
                self.assertFalse(remote_fh.closed)
                self.assertEqual(remote_fh.close(), 0)
                self.assertTrue(remote_fh.closed)
                self.assertEqual(remote_data, test_file_data)
            self.assertTrue(remote_fh.closed)
        finally:
            os.unlink(remote_filename)

    def test_sftp_write(self):
        self._auth()
        sftp = self.session.sftp_new()
        sftp.init()
        data = b"test file data"
        remote_filename = os.sep.join([os.path.dirname(__file__),
                                       "remote_test_file"])
        mode = 0666
        with sftp.open(remote_filename,
                       os.O_CREAT | os.O_WRONLY,
                       mode) as remote_fh:
            remote_fh.write(data)
        with open(remote_filename, 'rb') as fh:
            written_data = fh.read()
        _stat = os.stat(remote_filename)
        try:
            self.assertEqual(stat.S_IMODE(_stat.st_mode), 420)
            self.assertTrue(fh.closed)
            self.assertEqual(data, written_data)
        except Exception:
            raise
        finally:
            os.unlink(remote_filename)

    def test_sftp_attrs_cls(self):
        attrs = SFTPAttributes.new_attrs(None)
        self.assertIsInstance(attrs, SFTPAttributes)
        self.assertEqual(attrs.uid, 0)
        self.assertEqual(attrs.gid, 0)
        attrs.flags = 1
        attrs.type = 2
        attrs.size = 3
        attrs.uid = 4
        attrs.gid = 5
        attrs.permissions = 6
        attrs.atime64 = 7
        attrs.atime = 8
        attrs.atime_nseconds = 9
        attrs.createtime = 10
        attrs.createtime_nseconds = 11
        attrs.mtime64 = 12
        attrs.mtime = 13
        attrs.mtime_nseconds = 14
        attrs.extended_count = 15
        self.assertEqual(attrs.flags, 1)
        self.assertEqual(attrs.type, 2)
        self.assertEqual(attrs.size, 3)
        self.assertEqual(attrs.uid, 4)
        self.assertEqual(attrs.gid, 5)
        self.assertEqual(attrs.permissions, 6)
        self.assertEqual(attrs.atime64, 7)
        self.assertEqual(attrs.atime, 8)
        self.assertEqual(attrs.atime_nseconds, 9)
        self.assertEqual(attrs.createtime, 10)
        self.assertEqual(attrs.createtime_nseconds, 11)
        self.assertEqual(attrs.mtime64, 12)
        self.assertEqual(attrs.mtime, 13)
        self.assertEqual(attrs.mtime_nseconds, 14)
        self.assertEqual(attrs.extended_count, 15)
        del attrs

