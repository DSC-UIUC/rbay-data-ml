from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk
import numpy as np
from nltk.tokenize import word_tokenize


#complete
def main():
	nltk.download('punkt')
	model_pathname = "rec_alg.model"
	data_path = "data_list"
	classify_path = "classify_list.txt"
	output_pathname = "classified.txt"
	labels = [["machine", "learning"],["chatting"],["apple"]]

	data = load_data(data_path)
	#print(data)
	model = train_model(data)
	save_model(model, model_pathname)

	to_classify = load_data(classify_path)
	#print(to_classify)
	classify_results = classify(to_classify,model_pathname, labels)
	save_results(classify_results, output_pathname)






#TO-DO
def load_data(data_path):
	if(data_path == "classify_list.txt"):
		classif = [["machine", "learning"],["chatbots"]]
		test_data = classif#[word_tokenize("machine learning".lower()),word_tokenize("chatbots".lower())]
		return test_data
	else:
		data = ["I love machine learning. Its awesome.","I love coding in python", "I love building chatbots", "they chat amazingly well", "machine learning"]
		tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]
		return tagged_data

#complete
def train_model(data):
	max_epochs = 100
	vec_size = 20
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
def classify(to_classify, model_pathname,labels):
	model= Doc2Vec.load(model_pathname)
	ret_val = dict()
	#to find the vector of a document which is not in training data
	for term in to_classify[0]:
		sim_scores = np.array([-100.1])
		for choice in labels[0]:
			#print(choice)
			#print(term)
			res = model.wv.similarity(term,choice)
			sim_scores = np.append(sim_scores,res)
		idx = np.argmax(sim_scores)
		ret_val[term] = labels[idx]
	return ret_val

def save_results(classify_results,output_pathname):
	with open(output_pathname, "w") as f:
		for key in classify_results:
			line = "Best match for " + str(key) + " is " + str(classify_results[key]) + "!"
			f.write(line)
			f.write("\n")


def save_model(model,model_file):
	model.save(model_file)
	print('Model saved in ' + model_file + '!')

if __name__ == '__main__':
	main()
