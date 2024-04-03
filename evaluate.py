"""
	Evaluate an existing prediction file
	Create a new prediction file for specified languages
	Evaluates overall and per language accuracies.
"""
import json
import argparse
from preprocess import read_lines, read_labels, read_eng_labels, read_pred_labels
from predict import predict

MAX_NGRAM = 3
PRED_FILE = 'y_pred.txt'

def evaluate(x_test, y_test, eng_labels, n=MAX_NGRAM, include_only=None, y_pred=None):
	"""
		Compute overall accuracy and language-specfic accuracy of predicted labels
		If y_pred is provided then predictions are not re-computed.
		if include_only is not None then, compute prediction for restricted labels, rather than on all labels
			: this gives better predictions	
	"""
	lines = read_lines(x_test)
	labels = read_labels(y_test)
	eng_labels = read_eng_labels(eng_labels)
	x, y, y_prime = [], [], []
	if y_pred is None:
		with open(PRED_FILE, 'w', encoding='utf-8') as fp:
			for line, label in zip(lines, labels):
				if (include_only is not None) and (label not in include_only):
					continue
				else:
					x.append(line)
					y.append(label)
					pred = predict(line, n, include_only=include_only)
					y_prime.append(pred)
					fp.write(json.dumps(pred, ensure_ascii=False)+"\n")
	else:
		pred_labels = read_pred_labels(y_pred)
		for line, a_label, p_label in zip(lines, labels, pred_labels):
			if (include_only is not None) and (label not in include_only):
				continue
			else:
				x.append(line)
				y.append(a_label)
				y_prime.append(p_label)

	match = []
	for actual, pred in zip(y, y_prime):
		if pred[0][0] == "unk" and (include_only is not None) and (actual not in include_only):
			match.append(1)
		else:
			match.append(actual == pred[0][0])

	print('Overall Accuracy: %.3f'%(sum(match)/len(match)))
	
	for lang in eng_labels:
		if (include_only is not None) and (lang not in include_only):
			continue
		else:
			l_match = [match for y, match in zip(y, match) if y==lang]
			l_acc = sum(l_match)/len(l_match)
			print("Language: ", lang, " Label: %15s"%eng_labels[lang], "Num test data: %3d"%len(l_match), " Accuracy: %.3f"%l_acc)


if __name__ == '__main__':

	parser = argparse.ArgumentParser(
			prog='Language Identification: Evaluator',
            description='Evaluate Predictions on text set.')

	parser.add_argument('-x', type=str, default='wili-2018/x_test.txt', help="path to txt file containing test input")
	parser.add_argument('-y', type=str, default='wili-2018/y_test.txt', help="path to txt file containing gold test labels")
	parser.add_argument('-p', type=str, default=None, help="path to txt file containing predicted test labels")
	parser.add_argument('-l', type=str, default='wili-2018/labels.csv', help="path to csv file containing all language labels")
	parser.add_argument('-i', type=str, default=None, nargs='*', help="language codes to predict from")
	args = parser.parse_args()

	evaluate(
		args.x, 
		args.y, 
		args.l, 
		include_only=args.i,
		y_pred=args.p
		)