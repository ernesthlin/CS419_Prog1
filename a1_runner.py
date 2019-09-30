import a1_lib
import os
import argparse
"""
Program Runner for Authentication and Access Control Mechanism Library
Group: Ernest Lin, David Tian, Justin Chan
"""
def main():
	# parse all the arguments to the client 
	parser = argparse.ArgumentParser(description = "ACM Library")
	parser.add_argument("-f","--filename", help = "Text file with commands", required = True)
	parser.add_argument("-p","--persist", help = "Name of file to store results in (WITHOUT EXTENSION)", required = False)

	args = vars(parser.parse_args())
	file_name = args["filename"]
	source_file = args["persist"]

	with open("./testfiles/{}".format(file_name), "r") as testfile_reader:
		line_list = testfile_reader.readlines()
	for line in line_list:
		tokens = line.strip().split(" ")
		if tokens[0] == "AddUser":
			print("Attempting to add (user, password): ({}, {})".format(tokens[1], tokens[2]))
			try:
				a1_lib.AddUser(tokens[1], tokens[2])
			except ValueError as e:
				print(str(e))
				print()
				continue
			print("Successfully added (user, password): ({}, {})".format(tokens[1], tokens[2]))
			a1_lib.print_users()

		elif tokens[0] == "Authenticate":
			print("Authenticating (user, password): ({}, {})".format(tokens[1], tokens[2]))
			result = a1_lib.Authenticate(tokens[1], tokens[2])
			print(result)
			a1_lib.print_users()

		elif tokens[0] == "AddUserToGroup":
			print("Attempting to add user {} to group {}".format(tokens[1], tokens[2]))
			try:
				usergroup_list = a1_lib.AddUserToGroup(tokens[1], tokens[2])
			except ValueError as e:
				print(str(e))
				print()
				continue
			print("Added user {} to group {}: {}".format(tokens[1], tokens[2], usergroup_list))
			a1_lib.print_users()
			a1_lib.print_groups()

		elif tokens[0] == "AddObjectToGroup":
			print("Attempting to add object {} to group {}".format(tokens[1], tokens[2]))
			objectgroup_list = a1_lib.AddObjectToGroup(tokens[1], tokens[2])
			print("Object {} is now in group {}: {}".format(tokens[1], tokens[2], objectgroup_list))
			a1_lib.print_groups(is_user = False)

		elif tokens[0] == "AddAccess":
			if len(tokens) == 3:
				tokens.append(None)
			objectgroupname = "ALL_GROUPS" if len(tokens) == 3 else tokens[3]
			print("Adding access for user group {} to perform operation \"{}\" on object group {}".format(tokens[2], tokens[1], objectgroupname))
			try:
				access_controls_list = a1_lib.AddAccess(tokens[1], tokens[2], tokens[3])
			except ValueError as e:
				print(str(e))
				print()
				continue
			print("Added access for user group {} on object group {} for operation {}: {}".format(tokens[2], objectgroupname, tokens[1], access_controls_list))
			a1_lib.print_groups()
			a1_lib.print_groups(is_user = False)
			a1_lib.print_accesscontrols()

		elif tokens[0] == "CanAccess":
			if len(tokens) == 3:
				tokens.append(None)
			objectname = "NO_SPECIFIC" if len(tokens) == 3 else tokens[3]
			print("Checking access for user {} to perform operation \"{}\" on object {}".format(tokens[2], tokens[1], objectname))
			try:
				result = a1_lib.CanAccess(tokens[1], tokens[2], tokens[3])
			except ValueError as e:
				print(str(e))
				print()
				continue
			if result:
				print("User {} can {} object {}".format(tokens[2], tokens[1], objectname))
			else:
				print("User {} cannot {} object {}".format(tokens[2], tokens[1], objectname))
			a1_lib.print_groups()
			a1_lib.print_groups(is_user = False)
			a1_lib.print_accesscontrols()

		else:
			raise IOError("File input is invalid, first argument on each line should be a command.")

		print()

	print("Final results")
	print("-" * 40)
	a1_lib.print_users()
	print("-" * 40)
	a1_lib.print_groups()
	print("-" * 40)
	a1_lib.print_groups(is_user = False)
	print("-" * 40)
	a1_lib.print_accesscontrols()


main()