import hashlib
import bcrypt
import os
import hashlib, uuid

passwd = 'password'
#passwd = bytes(passwd, 'utf-8')
salt = bcrypt.gensalt()
#salt = uuid.uuid4().hex
#hashed = bcrypt.hashpw(passwd, salt)
hashed = hashlib.sha256(str.encode(passwd) + salt).hexdigest()
print("\nHashed Password:  ", hashed)

new_passwd = 'password'
salt2 = bcrypt.gensalt()
hashed2 = hashlib.sha256(str.encode(new_passwd) + salt).hexdigest()
print("\nNew Hashed Password:  ", hashed2)

if hashed2 == hashed:
    print('True')
else:
    print('False')




#hashed = hashlib.sha512(pswd + salt).hexdigest()
#print("Hashed Password:  ", hashed)

