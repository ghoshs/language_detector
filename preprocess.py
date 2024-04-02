import re
import csv
import unicodedata

def read_lines(file):
	lines = []
	with open(file, encoding='utf-8') as fp:
		for line in fp:
			lines.append(preprocess(line.strip()))
	return lines


def read_labels(file):
	labels = []
	with open(file, encoding='utf-8') as fp:
		for line in fp:
			labels.append(line.strip())
	return labels


def read_eng_labels(file):
	language_eng_labels = {}
	with open(file, encoding='utf-8') as f_label:
		reader = csv.DictReader(f_label, delimiter=';')
		language_eng_labels = {row['Label']: row['English'] for row in reader}
	return language_eng_labels


def preprocess(text):
	norm = unicodedata.normalize('NFKC', text)
	# replace punctuations/digits/extra white spaces with empty string
	clean = re.sub(r'[^\w\s]', '', norm)
	clean = re.sub(r'[\d]', '', clean)
	clean = ' '.join(clean.split())
	return clean


if __name__ == '__main__':
	orig = "This is here, to test 1st pre-processing of 10 upcoming languages.. Be 100% prepared!"
	print("Orig text: ", orig, "\nPrep text: ", preprocess(orig))
	orig = "Dies ist hier, um die 1. Vorverarbeitung von 10 aufkommenden Sprachen zu testen.. Seien Sie 100% vorbereitet!"
	print("Orig text: ", orig, "\nPrep text: ", preprocess(orig))
	orig = "Isto é aqui, para testar o 1º pré-processamento de 10 línguas futuras.. Esteja 100% preparado!"
	print("Orig text: ", orig, "\nPrep text: ", preprocess(orig))
	orig = "Αυτό είναι εδώ, για να δοκιμάσουμε την 1η προεπεξεργασία 10 επερχόμενων γλωσσών.. Να είστε 100% προετοιμασμένοι!"
	print("Orig text: ", orig, "\nPrep text: ", preprocess(orig))
	orig = "এটি এখানে, 10টি আসন্ন ভাষার প্রথম প্রি-প্রসেসিং পরীক্ষা করার জন্য।। 100% প্রস্তুত থাকুন!"
	print("Orig text: ", orig, "\nPrep text: ", preprocess(orig))
	orig = "앞으로 나올 10개 언어의 1차 전처리를 테스트하기 위해 왔습니다.. 100% 준비하세요!"
	print("Orig text: ", orig, "\nPrep text: ", preprocess(orig))
