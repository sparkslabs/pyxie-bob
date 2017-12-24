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

from django.core.management.templates import TemplateCommand
import re
import random
import pyxiebob.settings as settings
from django.contrib.auth.models import Group, User
from pyxiebob.models import UserProfile, FacilitatorRequest
from pyxiebob.random_phrase_generator import random_username, random_password

class Command(TemplateCommand):
    help = "Creates a number of users with randomised names and passwords"

    def handle(self, user_count_str="1", **options):
        MAXIMUM_USERS_TO_CREATE = 40
        if not re.match(r'^\d+$', user_count_str):
            print "Usage: python manage.py <number of users to create>"
            exit()

        user_count = int(user_count_str)
        if user_count == 1:
            print "Creating 1 user"
        if user_count > MAXIMUM_USERS_TO_CREATE:
            print "Cannot create more than {0} users".format(MAXIMUM_USERS_TO_CREATE)
            exit()
        else:
            print "Creating {0} users".format(user_count)

        facilitator = self.create_facilitator()
        facilitator_profile = self.saved_profile_for_user(facilitator)

        for user_index in range(1, user_count+1):
            username = random_username()
            password = random_password()

            new_user = User(username=username)
            new_user.set_password(password)
            new_user_profile = self.saved_profile_for_user(new_user)
            new_user_profile.facilitators.add(facilitator_profile)

            print "  {0}: {1} (PW: {2}, ID: {3})".format(user_index, username, password, new_user.id)

    # Returns a saved profile for the user
    def saved_profile_for_user(self, user):
        if not user.pk:
            user.save()
        (user_profile, user_profile_created) = UserProfile.objects.get_or_create(pk=user.id, user=user)
        if user_profile_created:
            user_profile.save()
        return user_profile

    def create_facilitator(self):
        username = random_username()
        password = random_password()

        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()

        facilitators = Group.objects.get(name='facilitators')
        facilitators.user_set.add(new_user)
        print "FACILITATOR: {0}: (PW: {1}, ID: {2}))".format(username, password, new_user.id)

        return new_user
