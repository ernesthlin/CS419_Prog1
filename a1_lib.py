import pickle
"""
Authentication and Access Control Mechanism Library
Group: Ernest Lin, David Tian, Justin Chan
"""

users = {} # key is user string, value is password string
user_groups = {} # key is group name, value is set of participating users
object_groups = {} # key is group name, value is set of participating objects
access_controls = {} # key is operation name, value is a list of 2-item tuples that are (user group, object)


"""
Define a new user for the system along with the user’s password, both strings.

Test program:
AddUser myname mypassword

The program should report an error if the user already exists.
"""
def AddUser(user, password):
	user = str(user)
	password = str(password)
	# user exists
	if user in users.keys(): 
		raise ValueError("Error: user already exists")
	
	elif password == "":
		raise ValueError("Error: password cannot be empty")
	# user does not exist
	else: 
		users[user] = password


"""
Validate a user’s password by passing the username and password, both strings.

Test program:
Authenticate myname mypassword

The program should clearly report
- Success
- Failure: no such user
- Failure: bad password
"""
def Authenticate(user, password):
	user = str(user)
	password = str(password)
	# user exists
	if user in users.keys():
		# password is valid
		if password == users[user]:
			return "Success"
		# password is invalid
		raise ValueError("Error: incorrect password")
	# user doesn't exist
	raise ValueError("Error: user doesn't exist")


"""
Add a user to a user group. If the group name does not exist, it is created. 
If a user does not exist, the function should return an error.

Test program:
AddUserToGroup user usergroupname

The program should report
- Success & list all the users in that group
- Failure if the user does not exist
"""
def AddUserToGroup(user, groupname):
	user = str(user)
	groupname = str(groupname)
	# user doesn't exist
	if user not in users.keys():
		raise ValueError("Error: user doesn't exist")
	# user does exist
	# group name doesn't exist
	if groupname not in user_groups.keys():
		user_groups[groupname] = set()
	user_groups[groupname].add(user)
	return user_groups[groupname]


"""
Add an object to an object group. If the group name does not exist, it is created. 
The object can be any string.

Test program:
AddObjectToGroup objectname objectgroupname

The program should report
- Success & list all the objects in that group
"""
def AddObjectToGroup(objectname, groupname):
	objectname = str(objectname)
	groupname = str(groupname)
	# group name does not exist
	if groupname not in object_groups.keys():
		object_groups[groupname] = set()
	# add object to group name
	object_groups[groupname].add(objectname)
	return object_groups[groupname]


"""
Define an access right: a string that defines an access permission of a user group to an object group. 
The access permission can be an arbitrary string that makes sense to the service.

Test program:
AddAccess operation usergroupname [objectgroupname]

The program will accept two or three strings. If objectgroupname is missing, it is considered null and 
the specified user group is simply permitted access to the operation regardless of the object (or an object 
may not make sense for that operation).
"""
def AddAccess(operation, usergroupname, objectgroupname = None):
	operation = str(operation)
	usergroupname = str(usergroupname)
	objectgroupname = str(objectgroupname) if objectgroupname else None
	# user group doesn't exist
	if usergroupname not in user_groups.keys():
		raise ValueError("Error: user group doesn't exist")
	# object group doesn't exist
	if objectgroupname and objectgroupname not in object_groups.keys():
		raise ValueError("Error: object group doesn't exist")
	# operation doesn't exist
	if operation not in access_controls.keys():
		access_controls[operation] = []
	access_controls[operation].append((usergroupname, objectgroupname))
	return access_controls[operation]


"""
Test whether a user can perform a specified operation on an object. Optionally, an object may be NULL, in which 
case CanAccess allows access if a user is part of a group for an operation on which no object group was defined.

Test program: 
CanAccess operation user [object]

The program will check whether the user is allowed to perform the specified operation on the object. 
That means that there exists a valid access right for an operation where the user is in usergroupname and the 
object is in the corresponding objectgroupname. As with AddAccess, the program will accept two or three strings. 
If object is missing, it is considered null and the software allows access only if no object groups were 
defined for that {operation, usergroupname} set. Note that the parameters here are user names and object names, 
not user groups and object groups.
"""
def CanAccess(operation, user_name, object_name = None):
	operation = str(operation)
	user_name = str(user_name)
	object_name = str(object_name) if object_name else None
	# user doesn't exist
	if user_name not in users.keys():
		raise ValueError("Error: user doesn't exist")
	# user does exist
	# operation doesn't exist
	if operation not in access_controls.keys():
		return False
	# get list of user groups that the user is in
	valid_user_groups = [key for key, value in user_groups.items() if user_name in value]
	# object is "missing"
	if not object_name:
		return any([(pair[0] in valid_user_groups) for pair in access_controls[operation] if pair[1] == None])
	# object is not "missing"
	return any([(pair[0] in valid_user_groups) for pair in access_controls[operation] 
		if pair[1] == None or object_name in object_groups[pair[1]]])


def store_data():
	with open("./tables/mydata.pickle", "wb") as pickle_file:
		pickle.dump(users, pickle_file)
		pickle.dump(user_groups, pickle_file)
		pickle.dump(object_groups, pickle_file)
		pickle.dump(access_controls, pickle_file)


def load_data():
	with open("./tables/mydata.pickle", "rb") as pickle_file:
		users = pickle.load(pickle_file)
		user_groups = pickle.load(pickle_file)
		object_groups = pickle.load(pickle_file)
		access_controls = pickle.load(pickle_file)


def print_users():
	print("Users:")
	print_str = ", ".join(["({}, {})".format(pair[0], pair[1]) for pair in users.items()])
	print(print_str)


def print_groups(is_user = True):
	groups = user_groups if is_user else object_groups
	print_str = "\n".join(["{} = {}".format(pair[0], pair[1]) for pair in groups.items()])
	print(print_str)


def print_accesscontrols():
	print_str = "\n".join(["{}: ({}, {})".format(kv[0], pair[0], pair[1]) for kv in access_controls.items() for pair in kv[1]])
	print(print_str)