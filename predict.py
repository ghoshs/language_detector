import os
import json
from os import listdir
from preprocess import preprocess
from build_profile import build_profile


def load_profiles(profile_path):
	files = []
	profiles = {}

	for file in listdir(profile_path):
		if file.endswith('.json'):
			files.append(os.path.join(profile_path, file))

	for file in files:
		lang = file.split("/")[-1].split(".json")[0]
		with open(file, encoding="utf-8") as fp:
			profiles[lang] = json.load(fp)

	return profiles


def min_distance(profile, L, n):
	distances = {}
	for lang in L:
		p_chars = [char for char in profile['3gram'] if char in L[lang]['3gram']]
		# weighted overlap since unknown language predicts some overlap due to noise
		overlap = len(p_chars)/len(L[lang]['3gram'].keys())
		distances[lang] = 1 - overlap
	
	return sorted(distances.items(), key=lambda x: x[1])


def predict(text, n, profile_path="./profiles"):
	line = preprocess(text)
	profile = build_profile([line], n, 1)

	L = load_profiles(profile_path)

	langs = min_distance(profile, L, n)
	if langs[0][1] == 0:
		langs = [("unk", 1.0)] + langs
	print(langs, '\n',  text)
	return langs[0]


if __name__ == '__main__':
	orig = "Earth is the third planet from the Sun and the only astronomical object known to harbor life. This is enabled by Earth being a water world, the only one in the Solar System sustaining liquid surface water. Almost all of Earth's water is contained in its global ocean, covering 70.8% of Earth's crust."
	predict(orig, n=3)
	orig = "পৃথিবী সূর্য থেকে দূরত্ব অনুযায়ী তৃতীয়, সর্বাপেক্ষা অধিক ঘনত্বযুক্ত এবং সৌরজগতের আটটি গ্রহের মধ্যে পঞ্চম বৃহত্তম গ্রহ। সূর্য হতে এটির দূরত্ব প্রায় ১৫ কোটি কি.মি।এটি সৌরজগতের চারটি কঠিন গ্রহের অন্যতম।"
	predict(orig, n=3)
	orig = "Die Erde ist der dichteste, fünftgrößte und der Sonne drittnächste Planet des Sonnensystems. Sie ist Ursprungsort und Heimat aller bekannten Lebewesen. Ihr Durchmesser beträgt mehr als 12.700 Kilometer und ihr Alter etwa 4,6 Milliarden Jahre."
	predict(orig, n=3)
	orig = "지구(地球, 영어: Earth)는 태양으로부터 세 번째 행성이며, 조금 두꺼운 대기층으로 둘러싸여 있고, 지금까지 발견된 지구형 행성 가운데 가장 크다. 지구는 45억 6700만 년 전 형성되었으며, 용암 활동이 활발했던 지구와 행성 테이아의 격렬한 충돌로 생성되었을 달을 위성으로 둔다. 지구의 중력은 우주의 다른 물체, 특히 태양과 지구의 유일한 자연위성인 달과 상호작용한다."
	predict(orig, n=3)