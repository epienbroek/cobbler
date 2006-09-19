"""
A Cobbler System.

Copyright 2006, Red Hat, Inc
Michael DeHaan <mdehaan@redhat.com>

This software may be freely redistributed under the terms of the GNU
general public license.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""

import utils
import item
import cexceptions

class System(item.Item):

    def __init__(self,config):
        self.config = config
        self.clear()

    def clear(self):
        self.name = None
        self.profile = None # a name, not a reference
        self.kernel_options = ""
        self.ks_meta = ""

    def from_datastruct(self,seed_data):
        self.name = seed_data['name']
        self.profile = seed_data['profile']
        self.kernel_options = seed_data['kernel_options']
        self.ks_meta = seed_data['ks_meta']
        return self

    def set_name(self,name):
        """
        A name can be a resolvable hostname (it instantly resolved and replaced with the IP),
        any legal ipv4 address, or any legal mac address. ipv6 is not supported yet but _should_ be.
        See utils.py
        """
        if name == "default":
            self.name="default"
            return True
        new_name = utils.find_system_identifier(name)
        if not new_name:
            raise cexceptions.CobblerException("bad_sys_name")
        self.name = name  # we check it add time, but store the original value.
        return True

    def set_profile(self,profile_name):
        """
	Set the system to use a certain named profile.  The profile
	must have already been loaded into the Profiles collection.
	"""
        if self.config.profiles().find(profile_name):
            self.profile = profile_name
            return True
        raise cexceptions.CobblerException("exc_profile")

    def is_valid(self):
        """
	A system is valid when it contains a valid name and a profile.
	"""
        if self.name is None:
            return False
        if self.profile is None:
            return False
        return True

    def to_datastruct(self):
        return {
           'name'     : self.name,
           'profile'  : self.profile,
           'kernel_options' : self.kernel_options,
           'ks_meta'  : self.ks_meta,
        }

    def printable(self,id):
        buf =       "system %-4s     : %s\n" % (id, self.name)
        buf = buf + "profile         : %s\n" % self.profile
        buf = buf + "kernel options  : %s" % self.kernel_options
        buf = buf + "ks metadata     : %s" % self.ks_meta
        return buf

