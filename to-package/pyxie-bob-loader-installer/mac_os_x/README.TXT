HOW TO BUILD BBCBUG.DMG
==========================

Set up your build environment, as detailed below.

Run makedmg.sh

That's it.

BUILD ENVIRONMENT
=================

Install PySide 1.2.1 binaries and Qt 4.8 for Mac

	Brew installs may work for you, but I had trouble with directory permissions, and ultimately installed DMGs from here:

	http://qt-project.org/wiki/PySide_Binaries_MacOSX#99905e544954e0e23f71eec9df2c02e9

Install Py2app

	You will need to sudo this if your Python install is a system installation
	
	pip install -U py2app

Make sure you have the version of libusb that dfu-programmer expects

	http://sourceforge.net/projects/libusb/postdownload?source=dlp

	You're looking for libusb-compat-0.1.4

Install dylibbundler

	Dylibbundler is used to add libusb into the application bundle

	https://github.com/auriamg/macdylibbundler/

Install appdmg
	
	https://github.com/LinusU/node-appdmg (requires node install http://nodejs.org/)

LICENSE
=======

#
# Copyright 2016 British Broadcasting Corporation and Contributors(1)
#
# (1) Contributors are listed in the AUTHORS file (please extend AUTHORS,
#     not this header)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance this license (or the alternative
# license below).
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# This file is also alternatively licensed under the terms of the GPL
# version 2. You may obtain a copy of the license at:
#
#     http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
