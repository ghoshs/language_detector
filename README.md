# Language Profiler for Language Detection


This project builds a language profile from a set of training text written in one dominant language. 
Each profile is a JSON formatted dictionary of most frequent (>=10) unigrams, bigrams and trigrams. The relative frequency of an ngram is recorded by taking the ratio of the ngram frequency and the total occurrences of all ngrams of the same length.
Given a text of unknown language, all ngrams are extracted. These are then matched against known langugae profiles, and return the language with the minimum distance. 

This implementation is an adaptation of [_W. B. Cavnar and J. M. Trenkle, “N-gram-based text categorization,”_](https://dsacl3-2019.github.io/materials/CavnarTrenkle.pdf). Instead of computing an out-of-place distance between a known and an unknown profiles, a weighted sum is computed of all 3grams in the unknown text that occur on the known language, weighed by the relative frequency. Hence, more the number of frequent 3grams of a known language used by an unknown piece of text, higher is the overlap, resulting in lower distance. A dictionary of languages and their distance to the unknown text is returned sorted by least to highest distance. 

If the lowest distance to a known language is 1, then 'unk' is returned, which means that the system predicts the language as **unknown**. This is rarely the case, the more realistic being that the least distance is very close to 1. In this case a threshold can be computed on a validation set. 


## Dataset

The language profiles are built using the training data in the [WiLi-2018 dataset](https://arxiv.org/pdf/1801.07779.pdf) which provides 500 short texts per language for 235 languages collected from Wikipedia.

The test set also contains 500 short texts per language. The dataset is in the `wili-2018/` folder.

### Format

- `x_*.txt` files contain a text in one dominant language per line.
- `y_*.txt` files contain one language code per line, which is the gold label for the text in  the corresponding line in the `x_` file.
- `labels.csv` contains one row per language with the language code, English label and other keys.
- `pred_test.txt` contains predictions on each line corresponding to the text in `x_test.txt` file.

## Setup


Create a conda environment:

`conda create -n lang_detect python=3.10`

Activate it:

`conda activate lang_detect`

Clone this repo:

`git clone https://github.com/ghoshs/language_detector && cd language_detector`

Or, unzip this folder

Now you can run any of the following scripts to build, predict or evaluate the language detection system.

Download and unip the wiLi-2018 dataset

`wget https://zenodo.org/records/841984/files/wili-2018.zip && unzip wiLi-2018.zip -d wili-2018`

## Build Profile

You can build language profiles using the following commands:

`python build_profile.py` - build profiles of all 235 languages.

`python build_profile.py -i eng deu` - builds profiles of the mentioned languages `eng` (English) and `deu` (German) and saves them in the `./profiles/` folder as `eng.json` and `deu.json`, respectively.

## Predict

You can predict the language of a text using the following commands:

- `python predict.py -o "This is a piece of text"` - predicts the language from all profiles available in the `profiles/` folder.

- `python predict.py -o "Chute annaée-lo, la Normaundie n'est pus recouneue coume eun pais de Fraunce. Les treis généralitaé sount minchie et ole est pairotaée en chin parts :" -i nrm eng ben hin kor` - predicts the language from the included profiles only and returns the top-3 matches:
```
nrm :  Chute annaée-lo, la Normaundie n'est pus recouneue coume eun pais de Fraunce. Les treis généralitaé sount minchie et ole est pairotaée en chin parts : 

Top-3 Predictions:  [('nrm', 0.7851420720896339), ('eng', 0.9166214269308668), ('ben', 0.9971654737640423)]` - , here, English, German and Dutch.
```

## Evaluate

Generate the performance on test files. Faster when fewer language codes are used.

- `python evaluate.py -x wili-2018/x_test.txt -y wili-2018/y_test.txt -i eng deu ben`: Generates accuracy scores for English, German and Bengali language texts. 

```
Overall Accuracy: 0.954
Language:  ben  Label:         Bengali Num test data: 500  Accuracy: 0.878
Language:  deu  Label:          German Num test data: 500  Accuracy: 0.990
Language:  eng  Label:         English Num test data: 500  Accuracy: 0.994
```

- `python evaluate.py`: Generates accuracy scores for all languages from the prediction file.

- The prediction overall accuracy (for 235 languages, and average of 62 texts per language) for the first 14703 lines in the test file `wili-2018/x_test.txt` is `0.886`. This increases with decreasing label space.

__Note__: Evaluating on all 235 languages takes time since the prediction function is not optimized. Evaluating 500 texts for a language takes an average of 2 mins.


