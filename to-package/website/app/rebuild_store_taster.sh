#!/bin/bash
#
# Copyright 2016 British Broadcasting Corporation and Contributors(1)
#
# (1) Contributors are listed in the AUTHORS file (please extend AUTHORS,
#     not this header)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

mv db.sqlite3 _db.sqlite3
rm ./pyxiebob/migrations/0*

#/usr/bin/python2.7 manage.py flush -- fails

echo 0 > ../pyxie-bob-store/primary/highest.txt
chmod 777 ../pyxie-bob-store/primary/highest.txt
rm ../pyxie-bob-store/pending/*.py
rm -f ../pyxie-bob-store/compiled/*hex ../pyxie-bob-store/compiled/*py
rm -f ../pyxie-bob-store/primary/*json

python manage.py syncdb
#sparkle - taqcrwt
/usr/bin/python2.7 manage.py setup_system
/usr/bin/python2.7 manage.py import_tutorials tutorial_source/
/usr/bin/python2.7 manage.py create_users 40 > /tmp/usernames_and_passwords.txt

for i in `seq 1 20`; do
     echo "-------------------------------------" | tee -a /tmp/usernames_and_passwords.txt
     echo "Class $i" | tee -a /tmp/usernames_and_passwords.txt
     echo "=========" | tee -a /tmp/usernames_and_passwords.txt
     /usr/bin/python2.7 manage.py create_users 40 | tee -a /tmp/usernames_and_passwords.txt
done
chmod a+rwx db.sqlite3
sudo apachectl restart

