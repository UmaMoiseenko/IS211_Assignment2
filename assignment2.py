import argparse
import csv
import datetime
import logging
import urllib2

# test URL:
# https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv

def main():
	def downloadData(url):
		content = urllib2.urlopen(url)
		return content

	def processData(content):
		dictionary = csv.reader(content)
		keys = dictionary.next()
		dateFormat = '%d/%m/%Y'
		linenum=1
		result = {}

		dictionary = [dict(zip(keys, row)) for row in dictionary]

		for row in dictionary:
			try:
				birthday = datetime.datetime.strptime(row['birthday'], dateFormat)
			except:
				logger.error('Error processing line #%s for ID #%s' % (linenum, row['id']))

			result[int(row['id'])] = (row['name'], row['birthday'])
			linenum+=1

		return result

	def displayPerson(id, personData):
		try:
			dateFormat = '%d/%m/%Y'
			birthday = datetime.datetime.strptime(personData[id][1], dateFormat) 
			birthday = '%s-%02d-%02d' % (birthday.year, birthday.month, birthday.day)
			name = personData[id][0]
			print 'Person #%s is %s with a birthday of %s' % ( id, name, birthday)
		except:
			print "No user found with that id"


	url_parser = argparse.ArgumentParser()
	url_parser.add_argument("--url", help='enter URL to CSV file', type=str)
	args = url_parser.parse_args()
	logging.basicConfig(filename='errors.log',level=logging.ERROR)
	logger = logging.getLogger('assignment2')

	if args.url:
		try:
			csvData = downloadData(args.url)
			personData = processData(csvData)
			prompt = "Enter number for ID lookup (for exit enter zero or negative number): "
			boolVal = True
			
			while boolVal:

				try:
					userInput = int(raw_input(prompt))

				except:
					print 'Plese enter a number'
					continue

				if userInput > 0:
					displayPerson(userInput, personData)

				else:
					print "Bye"
					boolVal = False
		except:
			print "Invalid URL"
	else:
		print "Print --help to see more details. Bye"

if __name__ == "__main__":
	main()
