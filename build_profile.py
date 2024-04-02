import os
import json
from collections import defaultdict
from prepare_data import prepare_data

MAX_NGRAM = 3
PATH = './profiles'

def one_gram_frequency(lines):
	one_gram_dict = defaultdict(int)
	for line in lines:
		for char in line:
			# code_point = ord(char)
			one_gram_dict[char] += 1
			
	return one_gram_dict


def ngram_frequency(lines, n=2):
	ngram_dict = defaultdict(int)
	for line in lines:
		if len(line) < n:
			return ngram_dict
		for idx in range(len(line)-n+1):
			ngram = line[idx:idx+n]
			# code_point_tuple = ";".join([ord(char) for char in ngram])
			ngram_dict[ngram] += 1

	return ngram_dict


def build_profile(lang, lines, max_n=1):
	lang_profile = {}
	assert max_n <= MAX_NGRAM

	lang_profile['1gram'] = one_gram_frequency(lines)
	if max_n > 1:
		for n in range(2,max_n+1):
			lang_profile[str(n)+'gram'] = ngram_frequency(lines, n=2)
	print(lang_profile)
	return lang_profile


def save_profile(lang_profile, lang):
	file = os.path.join(PATH, lang+'.json')
	with open(file, 'w') as fp:
		json.dump(lang_profile, fp, ensure_ascii=False)
		print('Language profile saved at: ', file)


if __name__ == '__main__':
	_, langugae_lines, _ = prepare_data(
			'wili-2018/x_train.txt', 
			'wili-2018/y_train.txt', 
			'wili-2018/labels.csv', 
			['ben', 'deu', 'eng'])
	for lang, lines in langugae_lines.items():
		lang_profile = build_profile(lang, lines[0:5], 3)
		save_profile(lang_profile, lang)