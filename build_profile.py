"""
Creates a language profile from input texts in a dominant language.
"""

import os
import json
import argparse
from collections import defaultdict
from prepare_data import prepare_data

MAX_NGRAM = 3
PATH = './profiles'
MIN_FREQUENCY = 10

def one_gram_frequency(lines, min_freq):
	"""
		Return a dict of 1-gram relative frequencues
		all 1-grams with frequency < min_freq are discarded  
	"""
	one_gram_dict = defaultdict(int)
	for line in lines:
		for char in line:
			one_gram_dict[char] += 1
	one_gram_dict = {char: freq for char, freq in one_gram_dict.items() if freq >= min_freq}
	sum_freq = sum([freq for freq in one_gram_dict.values()])
	one_gram_dict = {char: freq/sum_freq for char, freq in one_gram_dict.items()}
	return one_gram_dict


def ngram_frequency(lines, n, min_freq):
	"""
		Return a dict of n-gram relative frequencues
		all n-grams with frequency < min_freq are discarded  
	"""
	ngram_dict = defaultdict(int)
	for line in lines:
		if len(line) < n:
			continue
		for idx in range(len(line)-n+1):
			ngram = line[idx:idx+n]
			ngram_dict[ngram] += 1
	ngram_dict = {char: freq for char, freq in ngram_dict.items() if freq >= min_freq}
	sum_freq = sum([freq for freq in ngram_dict.values()])
	ngram_dict = {char: freq/sum_freq for char, freq in ngram_dict.items()}
	assert all([f <= 1.0 for f in ngram_dict.values()])
	return ngram_dict


def build_profile(lines, max_n=1, min_freq=10):
	"""
		Return a dict of relative frequencies
		level-one keys are: '1gram', '2gram', .. upto '<MAX_NGRAM>gram'
		level-one values are dicts of relative frequency distributions.
	"""
	lang_profile = {}
	assert max_n <= MAX_NGRAM

	lang_profile['1gram'] = one_gram_frequency(lines, min_freq)
	if max_n > 1:
		for n in range(2,max_n+1):
			lang_profile[str(n)+'gram'] = ngram_frequency(lines, n, min_freq)
	return lang_profile


def save_profile(lang_profile, lang):
	"""
		Save profile to be used during runtime prediction
	"""
	file = os.path.join(PATH, lang+'.json')
	with open(file, 'w') as fp:
		json.dump(lang_profile, fp, ensure_ascii=False)
		print('Language profile saved at: ', file)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
			prog='Language Identification: Profile Builder',
            description='Build a profile for specified or all languages from wili-2018/labels.csv.')

	parser.add_argument('-x', type=str, default='wili-2018/x_train.txt', help="path to txt file containing training input")
	parser.add_argument('-y', type=str, default='wili-2018/y_train.txt', help="path to txt file containing training labels")
	parser.add_argument('-l', type=str, default='wili-2018/labels.csv', help="path to csv file containing all language labels")
	parser.add_argument('-i', type=str, default=None, nargs='*', help="language codes to include")
	args = parser.parse_args()

	_, langugae_lines, _ = prepare_data(
			args.x, 
			args.y, 
			args.l,
			args.i)
			
	for lang, lines in langugae_lines.items():
		lang_profile = build_profile(lines, MAX_NGRAM, MIN_FREQUENCY)
		save_profile(lang_profile, lang)