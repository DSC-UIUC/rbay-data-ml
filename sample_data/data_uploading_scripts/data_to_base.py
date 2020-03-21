import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import importlib
from profile import Student_Profile
import time
import sys

def main():
	if(len(sys.argv) < 2):
		print("Incorrect usage")
		print(sys.argv)
		return
	name = single_name(sys.argv)

	
	default_app = firebase_admin.initialize_app()
	db = firestore.client()
	
	sp = Student_Profile(name)
	db.collection('studenttest6').document(name).set(sp.to_dict())
	print('Added: ' + name)

def single_name(system_input):
	final_name = ""
	for i in range(1, len(system_input)):
		if (i == 1):
			final_name = final_name + system_input[i]
		else:
			final_name = final_name + " " + system_input[i]
	return final_name

if __name__ == '__main__':
	main()


