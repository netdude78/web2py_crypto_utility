#!/usr/bin/env python
# coding: utf8

#!/usr/bin/env python

#***************************************************************************
# *                                                                         *
# *  Web2Py Cryptography Helper                                             * 
# *  Copyright (C) 2014                                                     *
# *  Dave Stoll dave<dot>stoll<at>gmail<dot>com                             *
# *                                                                         *
# *  This program is free software: you can redistribute it and/or modify   *
# *  it under the terms of the GNU General Public License as published by   *
# *  the Free Software Foundation, either version 3 of the License, or      *
# *  (at your option) any later version.                                    *
# *                                                                         *
# *  This program is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
# *  GNU General Public License for more details.                           *
# *                                                                         *
# *  You should have received a copy of the GNU General Public License      *
# *  along with this program.  If not, see <http://www.gnu.org/licenses/>.  *
# *                                                                         *
# ***************************************************************************


"""
   Crpytography Functions
   authors:    Dave Stoll <dave.stoll@gmail.com>
"""
from Crypto.Cipher import AES
from Crypto import Random
import base64, os

class SjCrypt(object):
    BLOCK_SIZE = 16
    MODE = AES.MODE_CFB
    
    def __init__(self, request=None):
        """
        Default constructor for use in web2py.
        Set up system-wide symmetric encryption key
        """
        if request:
            filename = os.path.join(request.folder,'private','encryption.secret')
            if not os.path.exists(filename): 
                key = Random.get_random_bytes(32)
                open(filename,'w').write(key)
                self.secret = open(filename,'r').read().strip()            
        else:
            # this is only for testing.  Random key... do NOT use this way
            self.secret = Random.get_random_bytes(32)
            
    def crypt(self, inmsg):
        """
        encryption method.
        
        crypt(string message)
        Returns a base64 encoded encrypted text
        """
        
        # first set up the initialization vector
        # this should be done for each encryption
        iv=Random.get_random_bytes(self.BLOCK_SIZE)
        
        # now get a cipher object.
        # very important to do this each time you call crypt or decrypt
        c = AES.new(self.secret, self.MODE, iv)
        
        #encrypt the incoming message
        msg = c.encrypt(inmsg)
        
        #prepend the IV to the msg
        encrypted_bytes=iv+msg
        
        #return the base64 encoded string
        return base64.urlsafe_b64encode(encrypted_bytes)
        
    def decrypt(self, inmsg):
        """
        decryption method.
        
        decrypt(string message)
        Takes a base64.urlsafe_b64encoded string as the only argument
        
        return the decrypted string
        """
        
        # first we must decode the incoming message
        encrypted_bytes = base64.urlsafe_b64decode(inmsg)
        
        # next split the incoming message to obtain iv and data
        # the IV is the first BLOCK_SIZE bytes
        iv, msg = (encrypted_bytes[:self.BLOCK_SIZE], encrypted_bytes[self.BLOCK_SIZE:])
        
        # now get a cipher object.
        # very important to do this each time you call crypt or decrypt
        c = AES.new(self.secret, self.MODE, iv)
        
        # decrypt the message and return it all together
        return c.decrypt(msg)
        

def test():
    """
    this will test the class
    """
    print 'Testing cryptography'
    msg = 'the british are coming'
    
    c = SjCrypt()
    print "msg before encryption: " + msg
    
    crypted = c.crypt(msg)
    print "encrypted message: " + crypted    

    decrypted = c.decrypt(crypted)
    print "decrypted message: " + decrypted
    
    assert(msg == decrypted), "Decrypted message does not match original."
    print "Test successful!"
    
if __name__ == "__main__":
    test()