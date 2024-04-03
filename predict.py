"""
	Computes the distance of unknown text to existing language profiles.
	Returns a dict of language codes and their distances, sorted in incresing order of distance.
"""
import os
import sys
import json
import argparse
from os import listdir
from preprocess import preprocess
from build_profile import build_profile


MAX_NGRAM = 3
PATH = './profiles'


def load_profiles(profile_path, include_only):
	"""
		Read JSON profiles of languges stored in `./profiles/` directory
		If include_only is not None, returns profiles of the specified languages
	"""
	files = []
	profiles = {}

	for file in listdir(profile_path):
		if file.endswith('.json'):
			files.append(os.path.join(profile_path, file))

	for file in files:
		lang = file.split("/")[-1].split(".json")[0]
		if (include_only is not None) and (lang not in include_only):
			continue
		with open(file, encoding="utf-8") as fp:
			profiles[lang] = json.load(fp)

	return profiles


def min_distance(profile, L, n):
	"""
	Given profile of an unknown text and a dict of known language profiles L,
	Return a dict of languages and their distance.

	"""
	distances = {}
	for lang in L:
		## non-weighted overlap function
		##	: sensitive to noise
		# p_chars = [char for char in profile['3gram'] if char in L[lang]['3gram']]
		# overlap = len(p_chars)/len(L[lang]['3gram'].keys())

		## weighted overlap since unknown language predicts some overlap due to noise
		overlap = sum([L[lang]['3gram'][char] for char in profile['3gram'] if char in L[lang]['3gram']])
		distances[lang] = 1 - overlap
	
	return sorted(distances.items(), key=lambda x: x[1])


def predict(text, n=MAX_NGRAM, profile_path=PATH, include_only=None):
	line = preprocess(text)
	profile = build_profile([line], n, 1)

	L = load_profiles(profile_path, include_only)

	langs = min_distance(profile, L, n)
	if langs[0][1] == 1.0:
		langs = [("unk", 1.0)] + langs
	return langs


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
			prog='Language Identification: Language Label Predictor',
            description='Predict language code of the input text.')

	parser.add_argument('-o', type=str, help="Original text")
	parser.add_argument('-i', type=str, default=None, nargs='*', help="language codes to predict from")
	args = parser.parse_args()

	langs = predict(args.o, include_only=args.i)
	top_3 = min(3, len(args.i)) if args.i is not None else 3
	print(langs[0][0], ": ",  args.o, "\n")
	print("Top-3 Predictions: ", langs[0: top_3])

	# orig = "Earth is the third planet from the Sun and the only astronomical object known to harbor life. This is enabled by Earth being a water world, the only one in the Solar System sustaining liquid surface water. Almost all of Earth's water is contained in its global ocean, covering 70.8% of Earth's crust."
	# langs = predict(orig, n=3, include_only=['eng','ben','deu'])
	# print(langs[0], "\n",  args.o, "\n\n")
	
	# orig = "পৃথিবী সূর্য থেকে দূরত্ব অনুযায়ী তৃতীয়, সর্বাপেক্ষা অধিক ঘনত্বযুক্ত এবং সৌরজগতের আটটি গ্রহের মধ্যে পঞ্চম বৃহত্তম গ্রহ। সূর্য হতে এটির দূরত্ব প্রায় ১৫ কোটি কি.মি।এটি সৌরজগতের চারটি কঠিন গ্রহের অন্যতম।"
	# langs = predict(orig, n=3, include_only=['eng','ben','deu'])
	# print(langs[0], "\n",  args.o, "\n\n")
	
	# orig = "Die Erde ist der dichteste, fünftgrößte und der Sonne drittnächste Planet des Sonnensystems. Sie ist Ursprungsort und Heimat aller bekannten Lebewesen. Ihr Durchmesser beträgt mehr als 12.700 Kilometer und ihr Alter etwa 4,6 Milliarden Jahre."
	# langs = predict(orig, n=3, include_only=['eng','ben','deu'])
	# print(langs[0], "\n",  args.o, "\n\n")

	# orig = "지구(地球, 영어: Earth)는 태양으로부터 세 번째 행성이며, 조금 두꺼운 대기층으로 둘러싸여 있고, 지금까지 발견된 지구형 행성 가운데 가장 크다. 지구는 45억 6700만 년 전 형성되었으며, 용암 활동이 활발했던 지구와 행성 테이아의 격렬한 충돌로 생성되었을 달을 위성으로 둔다. 지구의 중력은 우주의 다른 물체, 특히 태양과 지구의 유일한 자연위성인 달과 상호작용한다."
	# langs = predict(orig, n=3, include_only=['eng','ben','deu'])
	# print(langs[0], "\n",  args.o, "\n\n")