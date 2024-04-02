from preprocess import read_lines, read_labels, read_eng_labels

def prepare_data(x_train, y_train, eng_labels, choose_labels=None):
	all_languages = []
	language_lines = {}
	language_eng_labels = {}
	
	language_eng_labels = read_eng_labels(eng_labels)
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