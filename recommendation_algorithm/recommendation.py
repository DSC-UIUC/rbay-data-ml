from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk
import nltk.data
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore
from google.cloud import storage
import numpy as np
import smart_open
from nltk import tokenize
import string
from nltk import word_tokenize
import gensim
import pytextrank
import spacy
import gzip
import logging
import os
import re
import nltk
from nltk.corpus import stopwords


def main():
	nltk.download('punkt')
	num_recs = 3

	default_app = firebase_admin.initialize_app()
	db = firestore.client()

	
	#model_name = get_model()
	model_name = "enwiki_dbow/doc2vec.bin" #exists for local testing 
	
	
	student_list, professor_list = get_students_and_professors(db)
	
	posting_list = get_postings(db)
	
	

	students, students_reqs, keywords_to_students = keyword_extract(student_list, 0)
	professors, keywords_to_professors = keyword_extract(professor_list, 1)
	postings, postings_reqs, keywords_to_postings = keyword_extract(posting_list, 2)
	
	
	
	student_recs = classify(students, students_reqs, model_name, postings, postings_reqs, num_recs)
	professor_recs = classify(professors, None, model_name, students, None, num_recs)
	student_prof_recs = classify(students, students_reqs, model_name, professors, None, num_recs)
	
	
	write_recs(student_recs, 0, keywords_to_students, None, keywords_to_postings,db)
	write_recs(professor_recs, 1, keywords_to_students, keywords_to_professors, None,db)
	write_recs(student_prof_recs, 2, keywords_to_students, keywords_to_professors, None, db)	

	

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
		

def classify(to_classify, to_classify_reqs, model_name, being_classify, being_classify_reqs, num_recs):
	model= Doc2Vec.load(model_name)
	ret_val = dict()
	unseen_score = 1/(len(model.wv.vocab))

	for student in to_classify:
		scores = np.array([-1.0])
		scores = np.delete(scores,0)

		for posting in being_classify:
			cur_score = 0.0

			if(to_classify_reqs != None and being_classify_reqs != None):
				if(not req_check(to_classify_reqs, being_classify_reqs)):
					continue
			for attr in student:
				term_score = 0.0

				for post_attr in posting:
					try:
						cur_sim = model.wv.n_similarity(attr,post_attr)
						term_score = term_score + cur_sim
					except KeyError:
						term_score =  term_score + unseen_score
						continue

				cur_score = cur_score + term_score

			cur_score = cur_score/(len(being_classify))
			scores = np.append(scores,cur_score)

		k = -1*num_recs
		top_k_idxs = scores.argsort()[k:][::-1]
		top = []
		for idx in top_k_idxs:
			top.append(being_classify[idx])
		temp = []
		for entity in student:
			temp.append(entity)
		tup_stud = tuple(temp)
		ret_val[tup_stud] = top	
		
		
	return ret_val


def save_results(classify_results,output_pathname):
	with open(output_pathname, "w") as f:
		for key in classify_results:
			line = "Best match for " + str(key) + " is " + str(classify_results[key]) + "!"
			f.write(line)
			f.write("\n")


def get_model():
	
	model_name = 'doc2vec.bin'
	spf1_name = 'doc2vec.bin.syn0.npy'
	spf2_name = 'doc2vec.bin.syn1neg.npy'
	storage_client = storage.Client()
	bucket = storage_client.bucket('research-bay.appspot.com')
	model = bucket.blob('wikipedia_based_model/doc2vec.bin') 
	model.download_to_filename(model_name)
	spf1 = bucket.blob('wikipedia_based_model/doc2vec.bin.syn0.npy') 
	spf1.download_to_filename(spf1_name)
	spf2 = bucket.blob('wikipedia_based_model/doc2vec.bin.syn1neg.npy') 
	spf2.download_to_filename(spf2_name)

	
	return model_name

def get_students_and_professors(db):
	all_profiles = db.collection("users").stream()
	profile_collec = db.collection("profiles")
	student_list = []
	professor_list = []
	for profile in all_profiles:
		raw_id = profile.id
		cur_prof = profile.to_dict()
		raw_person = profile_collec.document(raw_id).get()
		formatted_person = raw_person.to_dict()
		formatted_person['temp_id'] = raw_id
		if(cur_prof['is_student']):
			student_list.append(formatted_person)
		else:
			professor_list.append(formatted_person)
	return student_list, professor_list

def get_students(db):
	student_info_list = []
	all_students = db.collection("profiles").stream()
	formatted_students = []
	for student in all_students:
		cur_form = student.to_dict()
		if "year" not in cur_form:
			continue
		formatted_students.append(cur_form)
	return formatted_students

def get_professors(db):
	professor_info_list = []
	all_professors = db.collection("profiles").stream()
	formatted_professors = []
	for professor in all_professors:
		cur_form = professor.to_dict()
		if "year" in cur_form:
			continue
		formatted_professors.append(cur_form)
	return formatted_professors

def get_postings(db):
	posting_info_list = []
	all_postings = db.collection("postings").stream()
	formatted_postings = []
	for posting in all_postings:
		post_id = posting.id
		new_dict = posting.to_dict()
		new_dict['temp_id'] =post_id
		formatted_postings.append(new_dict)
	return formatted_postings


def keyword_extract(collection, type_s):
	if(type_s == 0):
		student_keywords = []
		student_req_info = []
		keywords_to_students = dict()
		for student in collection:
			cur_keywords = student['coursework']
			cur_reqs = dict()

			cur_reqs['coursework'] = student['coursework']
			cur_keywords = cur_keywords + student['skills']
			cur_keywords = cur_keywords + student['research_interests']
			cur_keywords = cur_keywords + gen_keyword_extract(student['about_me'])
			if(str(type(student['experience'])) == '<class \'dict\'>'):
				for expr in student['experience']:
					if(student['experience'][expr] == 'description'):
						cur_keywords = cur_keywords + gen_keyword_extract(student['experience'][expr]['description'])
			if(str(type(student['experience'])) == '<class \'list\'>'):
				for i in range(len(student['experience'])):		
					if(student['experience'][i] == 'description'):
						cur_keywords = cur_keywords + gen_keyword_extract(student['experience'][i])
			cur_reqs['major'] = student['major']
			cur_reqs['gpa'] = student['gpa']
			cur_reqs['year'] = student['year']

			student_keywords.append(cur_keywords)
			
			keywords_to_students[tuple(cur_keywords)] = student['temp_id']
			student_req_info.append(cur_reqs)

			

		return student_keywords,student_req_info, keywords_to_students

	elif(type_s == 1):
		professor_keywords = []
		keywords_to_professors = dict()

		for professor in collection:
			if('coursework' in professor):
				cur_keywords = professor['coursework']
			cur_keywords = cur_keywords + professor['research_interests']
			cur_keywords = cur_keywords + gen_keyword_extract(professor['about_me'])
			professor_keywords.append(cur_keywords)
			keywords_to_professors[tuple(cur_keywords)] = professor['temp_id']
			

		return professor_keywords, keywords_to_professors
	else:
		posting_keywords = []
		posting_req_info = []
		keywords_to_postings = dict()

		for posting in collection:
			cur_keywords = posting['tags']
			cur_reqs = dict()

			cur_keywords = cur_keywords + gen_keyword_extract(posting['description'])
			if('major' in posting['requirements']):
				cur_reqs['major'] = posting['requirements']['major']
			if('gpa' in posting['requirements']):
				cur_reqs['gpa'] = posting['requirements']['gpa']
			if('year' in posting['requirements']):
				cur_reqs['year'] = posting['requirements']['year']
			if('coursework' in posting['requirements']):
				cur_reqs['coursework'] = posting['requirements']['coursework']

			posting_keywords.append(cur_keywords)
			keywords_to_postings[tuple(cur_keywords)] = posting['temp_id']
			posting_req_info.append(cur_reqs)

		return posting_keywords, posting_req_info, keywords_to_postings

def write_recs(recs_list, type_o, keywords_to_students, keywords_to_professors, keywords_to_postings, db):
	if(type_o == 0):
		for student in recs_list:
			student_id = keywords_to_students[tuple(student)]
			rec_id_list = [keywords_to_postings[tuple(rec)] for rec in recs_list[student]]
			ref = db.collection('recommendations').document(student_id).set({"postings":rec_id_list})
			ref = db.collection('recommendations').document(student_id).set({"profiles":[]}, merge=True)
	elif(type_o == 1):
		for professor in recs_list:
			professor_id = keywords_to_professors[tuple(professor)]
			rec_id_list = [keywords_to_students[tuple(rec)] for rec in recs_list[professor]]
			ref = db.collection('recommendations').document(professor_id).set({"profiles":rec_id_list})
			ref = db.collection('recommendations').document(professor_id).set({"postings":[]}, merge=True)
	else:
		for student in recs_list:
			student_id = keywords_to_students[tuple(student)]
			rec_id_list = [keywords_to_professors[tuple(rec)] for rec in recs_list[student]]
			ref = db.collection('recommendations').document(student_id).set({"profiles":rec_id_list},merge=True)

def gen_keyword_extract(text):
	nlp = spacy.load("en_core_web_sm")
	keywords = []
	tr = pytextrank.TextRank()
	nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)
	doc = nlp(text)
	phrases = []
	for p in doc._.phrases:
	    phrases.append((p.rank, p.count, p.text))
	phrases = sorted(phrases, reverse=True)
	keywords = [x[2] for x in phrases]
	return keywords

def req_check(student, posting):
	for req in posting:
		if(req == 'major' and len(posting['major']) > 0):
			if(student['major'] not in posting['major']):
				return False
		if(req == 'gpa'):
			if(student['gpa'] < posting['gpa']):
				return False
		if(req == 'year'):
			if(student['year'] < posting['year']):
				return False
		if(req == 'coursework' and len(posting['coursework']) > 0):
			for course in posting['coursework']:
				if(course not in student['coursework']):
					return False
		return True


if __name__ == '__main__':
	main()
