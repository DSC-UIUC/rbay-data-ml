from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk
import nltk.data
import numpy as np
import smart_open
from nltk import tokenize
import string
from nltk import word_tokenize
import gensim


#complete
def main():
	nltk.download('punkt')
	model_pathname = "rec_alg.model"
	data_path = "data_list"
	classify_student_path = "classify_list.txt"
	classify_posting_path = "hehe.txt"
	output_pathname = "classified.txt"
	
	data = load_data(data_path, True)
	print(data)
	model = train_model(data)
	save_model(model, model_pathname)

	students = load_data(classify_student_path, False)
	postings = load_data(classify_posting_path, False)
	classify_results = classify(students,model_pathname, postings)
	save_results(classify_results, output_pathname)
	print("Program complete")


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
def load_data(data_path, build_model):
	if(build_model):
		fp = open(data_path)
		p = fp.read()
		data = tokenize.sent_tokenize(p)

		print(data)
		return [TaggedDocument(words=clean_text(s).split(), tags=[i]) for i, s in enumerate(data)]
	else:
		with open(data_path) as f:
			res = []
			for line in f:
				cur_entr = []
				words = line.split(',')
				for w in words:
					ms = w.split()
					cur_entr.append(ms)
				res.append(cur_entr)
			return res

#complete
def train_model(data):
	max_epochs = 100
	vec_size = 50
	alpha = 0.025
	model = Doc2Vec(size=vec_size,
	                alpha=alpha,
	                min_alpha=0.00025,
	                min_count=1,
	                dm =1)
	model.build_vocab(data)
	for epoch in range(max_epochs):
	    print('iteration {0}'.format(epoch))
	    model.train(data,
	                total_examples=model.corpus_count,
	                epochs=model.iter)
	    model.alpha -= 0.0002
	    model.min_alpha = model.alpha
	return model

#To-do
def classify(student_classify,model_pathname,posting_classify):
	model= Doc2Vec.load(model_pathname)
	ret_val = dict()

	for student in student_classify:
		scores = np.array([-1.0])
		scores = np.delete(scores,0)
		for posting in posting_classify:
			cur_score = 0.0
			for attr in student:
				term_score = 0.0
				for post_attr in posting:
					
					term_score = term_score + model.wv.n_similarity(attr,post_attr)
				cur_score = cur_score + term_score
			scores = np.append(scores,cur_score)
		top = posting_classify[np.argmax(scores)]
		
		temp = []
		for entity in student:
			val = tuple(entity)
			temp.append(val)
		tup_stud = tuple(temp)
		ret_val[tup_stud] = top			
		
	return ret_val

#done
def save_results(classify_results,output_pathname):
	with open(output_pathname, "w") as f:
		for key in classify_results:
			line = "Best match for " + str(key) + " is " + str(classify_results[key]) + "!"
			f.write(line)
			f.write("\n")


#done
def save_model(model,model_file):
	model.save(model_file)
	print('Model saved in ' + model_file + '!')

if __name__ == '__main__':
	main()
