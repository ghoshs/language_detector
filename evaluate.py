from preprocess import read_lines, read_labels, read_eng_labels


def evaluate(x_test, y_test, eng_labels):
	lines = read_lines(x_test)
	labels = read_labels(y_test)
	eng_labels = read_eng_labels(eng_labels)
	y = []
	for line in lines:
		y.append(predict(line))

	match = []
	for actual, pred in zip(y_test, y):
		match.append(actual == pred)

	print('Accuracy: %.3f'%(sum(match)/len(match)))