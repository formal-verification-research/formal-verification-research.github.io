while(True):
	myInput = input("Paste in the list of BibTeX names: ")

	print("Names are ")

	words = myInput.split()

	# hasFirst = false
	hasLast = False
	last = ""
	first = ""

	for word in words:
		if (word == 'and' or word == words[-1]):
			if (word == words[-1]):
				first += (word + " ")
				last = last[:-2] + " "
				print("and ", end = '')
			print(first + last, end = '')
			hasLast = False
			last = ""
			first = ""
		else:
			if not(hasLast):
				last += (word + " ")
				if (word[-1] == ','):
					hasLast = True
			else:
				first += (word + " ")

	print("\n")