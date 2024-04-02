import csv
from preprocess import preprocess

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


def prepare_data(x_train, y_train, labels, choose_labels=None):
	all_languages = []
	language_lines = {}
	language_eng_labels = {}
	with open(labels, encoding='utf-8') as f_label:
		reader = csv.DictReader(f_label, delimiter=';')
		language_eng_labels = {row['Label']: row['English'] for row in reader}
	all_languages = list(language_eng_labels.keys())
	lines = read_lines(x_train)
	labels = read_labels(y_train)
	for line, label in zip(lines, labels):
		if label in language_lines:
			language_lines[label].append(line)
		else:
			language_lines[label] = [line]
	if choose_labels is not None:
		all_languages = [lang for lang in all_languages if lang in choose_labels]
		language_lines = {lang: lines for lang, lines in language_lines.items() if lang in choose_labels}
		language_eng_labels = {lang: label for lang, label in language_eng_labels.items() if lang in choose_labels}
	print("Num labels: ", len(all_languages))
	print("Labels: ", all_languages)
	print("Num data per label:\n", '\n'.join([k+":"+str(len(v)) for k,v in language_lines.items()]))
	return all_languages, language_lines, language_eng_labels

if __name__ == '__main__':
	prepare_data('wili-2018/x_train.txt', 'wili-2018/y_train.txt', 'wili-2018/labels.csv', ['ben', 'deu', 'eng'])