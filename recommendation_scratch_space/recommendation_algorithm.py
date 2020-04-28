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
	#model_pathname = "recommendations.model"
	model_pathname = "enwiki_dbow/doc2vec.bin"
	classify_student_path = "classify_list.txt"
	classify_posting_path = "hehe.txt"
	output_pathname = "classified.txt"
	num_recs = 3
	
	
	#print('Loading Students and Postings...')
	students = load_data(classify_student_path)
	postings = load_data(classify_posting_path)
	#print('Students and Postings Loaded!')
	#print('Begin classification')
	classify_results = classify(students,model_pathname, postings, num_recs)
	save_results(classify_results, output_pathname)
	#print("Classification complete")
	

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


def load_data(data_path):
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
		

def classify(student_classify,model_pathname,posting_classify, num_recs):
	model= Doc2Vec.load(model_pathname)
	ret_val = dict()
	unseen_score = 1/(len(model.wv.vocab))
	#print(unseen_score)
	for student in student_classify:
		scores = np.array([-1.0])
		scores = np.delete(scores,0)
		for posting in posting_classify:
			cur_score = 0.0
			for attr in student:
				term_score = 0.0
				for post_attr in posting:
					try:
						cur_sim = model.wv.n_similarity(attr,post_attr)
						term_score = term_score + cur_sim
						#print('Score for ' + str(attr) + ' and ' + str(post_attr) + ' is ' + str(cur_sim))
					except KeyError:
						term_score =  term_score + unseen_score
						#print('Unseen word pair: ' + str(attr) + ',' + str(post_attr) + ' adding ' + str(unseen_score))
						continue
				cur_score = cur_score + term_score
			cur_score = cur_score/(len(posting_classify))
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


if __name__ == '__main__':
	main()
