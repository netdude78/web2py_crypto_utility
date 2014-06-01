web2py_crypto_utility
=====================

Simple AES encryption handler class for Web2Py.  Will allow encryption and 
decryption of data using an encryption secret stored in the application.  

Prequisites:
	* PyCrypto.  You must have PyCrypto installed on the system you intend
	to use this with.  On a Mac, compiling and installing PyCrypto under 
	Mavericks is a bit of a challenge.  There is a workaround available 
	if you need it.  If you can't find the workaround, reach out to me and
	I will point you in the right direction.


Background:
	This library will handle AES encryption and decryption using a cryto
	secret that is stored in the application's private/ folder.  The first
	time you create an object of the class AgCrypto, a random key will be
	created (only if there is not a file named encryption.secret) in private/.

	If you are going to be doing lots of encrypts and decrypts you may consider
	caching an AgCrypto object.  That way you are not waiting on the class to
	read the secret from disk.  Google the cache functions on the Web2Py doc site.
	Here is basically what you will put in one of your model/ files:

		from Cryptography import *
		crypto = cache.ram('crypto', lambda: AgCrypt(request), 3600)

	Make sure the Cryptography.py file is in your modules/ directory for this to work.
	If for some reason you already have a file with that name, change it.  The only thing
	that will be effected is the import statement.  This sample cache statement above will 
	expire the cached object after 1 hour.  You could set that number higher if your 
	installation required it.

Usage:

	Once you have created an object of type AgCrypt, there are two methods:
		crypt(msg)
		decrypt(msg)

		crypt will return a base64 encoded, AES encrypted string.  That string,
		when passed to decrypt(msg) will return the original cleartext message.

	Testing:
		To ensure your environment is set up properly, __main__ is implemented
		as a sort of unit test.  From the command line if you type python AgCrypto
		you should see something like this:

			$ python Cryptography.py
			Testing cryptography
			msg before encryption: the british are coming
			encrypted message: YlLxDxjDfwNj2-bUuDpBoUT_CeRzX4MOX_PBcUyORfo1tL0xBEg=
			decrypted message: the british are coming
			Test successful!		

		Keep in mind, your encrypted string is going to be different.  In fact,
		it will be different every time you execute the code this way.  If the
		__init__ method is not called as part of a Web2Py Request, a random secret
		is generated.  That random secret disappears and is never written to disk.

If you find bugs or have suggestions, feel free to fork the code and submit a merge 
request.  You can also get in contact with me at dave<dot>stoll<at>gmail<doc>com.