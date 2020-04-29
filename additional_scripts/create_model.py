from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk
import nltk.data
import numpy as np
import smart_open
from nltk import tokenize
import string
from nltk import word_tokenize
import gensim


def main():
	nltk.download('punkt')
	model_pathname = "recommendations.model"
	data_path = ["cleaned_dataset.txt"]
	
	print('Starting Data Loading....')
	data = load_data(data_path)
	print('Data Loaded.')
	print('Starting Model Training...')
	model = train_model(data)
	print('Model Training Complete.')
	save_model(model, model_pathname)
	print('Model Saved in ' + model_pathname)
	
	

TABLE_TRANS = str.maketrans({key: ' ' for key in string.punctuation})
TABLE_TRANS['.'] = ' . '
TABLE_TRANS['?'] = ' . '
TABLE_TRANS['!'] = ' . '
TABLE_TRANS[':'] = ' . '
TABLE_TRANS[';'] = ' . '
TABLE_TRANS['('] = ' '
TABLE_TRANS[')'] = ' '
TABLE_TRANS['['] = ' '
TABLE_TRANS[']'] = ' '
TABLE_TRANS[','] = ' '
TABLE_TRANS['{'] = ' '
TABLE_TRANS['}'] = ' '


def clean_text(s):
    words = str(s).lower().translate(TABLE_TRANS).split()
    return " ".join(words)

#turn files into TaggedDocs
def load_data(data_path_list):
	content = ''
	for file in data_path_list:
		fp = open(file)
		content = content + fp.read()
		fp.close()
	data = tokenize.sent_tokenize(content)
	return [TaggedDocument(words=clean_text(s).split(), tags=[i]) for i, s in enumerate(data)]

#complete
def train_model(data):
	max_epochs = 100
	vec_size = 50
	alpha = 0.025
	model = Doc2Vec(vector_size=vec_size,alpha=alpha,min_alpha=0.00025,min_count=1,dm =1)
	model.build_vocab(data)
	for epoch in range(max_epochs):
	    print('iteration ' + str(epoch))
	    model.train(data,total_examples=model.corpus_count,epochs=model.iter)
	    model.alpha -= 0.0002
	    model.min_alpha = model.alpha
	return model

#done
def save_model(model,model_file):
	model.save(model_file)
	print('Model saved in ' + model_file + '!')

if __name__ == '__main__':
	main()
