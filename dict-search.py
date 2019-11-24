import requests
import re
import sys
import nltk
from nltk.corpus import stopwords

def get_definition(word):
	word = word.lower()
	response = ''

	
	base_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
	api = "API-KEY-HERE"
	api_key = "?key=" + api
	
	if (api == "API-KEY-HERE"):
		return -1;

	full_api = base_url + word + api_key

	try:
		response = requests.get(full_api)
		response = response.json()
		response = str(response[0]['def'][0]['sseq'][0][0][1])
		
		word_definition = response.split('dt')[1]
		if (word_definition.find('],') != -1):
			word_definition = word_definition.split('],')[0]

		bc_index = word_definition.find('{bc}') 

		end_index = word_definition.find('}:') 
		end_index_1 = word_definition.find('\']]') 
		if (end_index_1 < end_index and end_index_1 > 0):
			end_index = end_index_1
		
		end_index_2 = word_definition.find('\'],')
		if (end_index_2 < end_index):
			end_index = end_index_2

		if (end_index == -1):
			end_index = len(word_definition)

		word_definition = word_definition[bc_index + 4 : end_index]

		word_definition = re.sub('\|.*?\|','|', word_definition)	
		word_definition = re.sub('{.*?\|','', word_definition)	
		word_definition = re.sub('{.*?}','', word_definition)	
		word_definition = re.sub('[^a-zA-Z ]+', '', word_definition)
		word_definition = re.sub(' +', ' ', word_definition)

		print("------------------")
		print("Definition of " + str(word) + ": " + word_definition)

		return word_definition
	except:
		return ''

def main(word):
	stop_words = set(stopwords.words('english')) 

	word_depth_value = 0

	known_words = set()
	known_words.add(word)

	unknown_words = set()
	word_definition = get_definition(word)
	if (word_definition == -1):
		print('This code can\'t be run without an API key!\nYou\'ll need an API key first. Visit: https://dictionaryapi.com/ and change the api variable to your API key.')
		return;

	word_definition_arr = word_definition.split(" ")
	for word in word_definition_arr:
		if word not in stop_words and len(word) > 1: 
			print("Adding word: " + str(word))
			unknown_words.add(word)

	while len(unknown_words) > 0:
		word = unknown_words.pop()
		known_words.add(word)
		word_definition = get_definition(word)
		word_definition_arr = word_definition.split(" ")
		
		for word in word_definition_arr:
			if word not in known_words and word not in unknown_words and word not in stop_words:
				unknown_words.add(word)
				word_depth_value += 1
		
		if word_depth_value % 50 is 0:
			print("NUM UNKNOWN WORDS: " + str(len(unknown_words)))
			print("NUM KNOWN WORDS: " + str(len(known_words)))

		print("Now I know " + str(word_depth_value) + str(" words!"))

	print("I needed to learn " + str(word_depth_value) + " words")

# To search for the word "hello", you can either run from the terminal as below.
# python3 dict-search.py hello
# Or you can update the word variable i.e. word = 'hello' and run python3 dict-search.py
if __name__ == '__main__':
	word = ''
	try:
		input_val = sys.argv[1]
		main(input_val)
	except:
		if (len(word) < 1):
			print("You'll need to input some word to search. Or you can update the variable in line 102.")
		else:
			main(word)