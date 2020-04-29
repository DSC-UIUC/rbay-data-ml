
<br />
<p align="center">
  <a href="https://github.com/DSC-UIUC/research-bay">
    <img src="https://github.com/DSC-UIUC/research-bay/blob/master/images/rbay_logo_long.png?raw=true" alt="Logo">
  </a>

  <h3 align="center">:mag_right: Research Bay <strong>Data/ML</strong></h3>

  <p align="center">
    A web platform for efficiently connecting students to research opportunities and professors
    <br />
    <a href="https://research-bay.web.app"><strong><< Live Website >></strong></a>
    <br />
    <br />
    Repository Links
    <br />
    <a href="https://github.com/DSC-UIUC/research-bay">Main</a>
    ·
    <a href="https://github.com/DSC-UIUC/rbay-frontend">Frontend</a>
    ·
    <a href="https://github.com/DSC-UIUC/rbay-backend">Backend</a>
    ·
    <a href="https://github.com/DSC-UIUC/rbay-data-ml">Data/ML</a>
  </p>
</p>

## Table of Contents

* [About Data-ML](#about-data-ml)
  * [DSC at UIUC](#dsc-at-uiuc)
* [Getting Started](#getting-started)
* [Documentation](#documentation)
  * [Core Features](#core-features)


## About Data-ML

This repository contains the code and documentation for Research Bay's Data/ML work, which mainly provides the basis for the search system and the
recommendation system for Research Bay. The code here reads the training model and information from the database to generate recommended postings and 
profiles for users. Additionally, it handles search functionality by.....

More information about Research Bay as an entire project is available at the [main repository](https://github.com/DSC-UIUC/research-bay).

### DSC at UIUC

The Research Bay project is built and maintained by student developers in Developer Student Club at the University of Illinois at Urbana-Champaign (DSC at UIUC) during the 2019-2020 school year. DSC at UIUC is an official branch of Google Developers' global [Developer Student Club program](https://developers.google.com/community/dsc).

## Getting Started

The recommendation system depends on the following libraries:
* [Gensim](https://radimrehurek.com/gensim/auto_examples/index.html)
* [NLTK](https://radimrehurek.com/gensim/auto_examples/index.html)
* [Numpy](https://numpy.org/)
* [PyTextRank](https://pypi.org/project/pytextrank/)
* [Smart-Open](https://pypi.org/project/smart-open/)

along with 

* [Firebase-Admin](https://firebase.google.com/docs/reference/admin)
* [Google-Cloud](https://cloud.google.com/docs)

These can be installed using a package manager such as pip, or directly from source.

The search algorithm depends on the following web service:
* [Algolia](https://www.algolia.com)

along with 

* [Cloud Firestore](https://cloud.google.com/firestore)
* [Google-Cloud](https://cloud.google.com)


Please refer to the Research Bay general setup guide [here](https://github.com/DSC-UIUC/research-bay/blob/master/README.md#getting-started).

## Documentation

The rest of this README contains the documentation for the recommondation system, the search system, and some additional scripts. Feel free to contact the Research Bay team at dscuiuc2@gmail.com with any questions or concerns.

### Core Features

The core features of Research Bay's Data/ML components are described below.

#### Search Engine

Our search algorithm uses Algolia's web service to accurately deliver search results to students and professors. We decided to use Algolia because it had seamless integration from our Cloud Firestore data collections to Algolia. Using their search service provides us with quick and accurate results for Research Bay. This was the process we went through to develop our search feature:

In order to build a fully functional search algorithm, we first had to figure out which collections in our Cloud Firestore database we wanted to allow for searching. Having decided that the postings and profiles collection both needed to be searched by professors and students, we needed to create or find a search algorithm that would take data from those two collections and give us the best response. As a team, we decided to use Algolia over other options like ElasticSearch because it had great documentation that supported integration from our Cloud Firestore data collections to Algolia’s service.

Next, we added two cloud functions that updated the indices for our postings and profiles collection in Algolia. Once our data was indexed, we created a cloud function that used Algolia’s API to call a search function that returned the responses given our queries. However, we found that some of the data Algolia returned had unnecessary fields. To fix this, we created our own javascript objects and passed in the data that was deemed useful to us and returned that to the frontend instead. In doing so, our cloud functions provided an extra layer of abstraction allowing the framework as a whole to be seamless.


#### Recommendation System

The recommendation system provides a way to be able to allow students to see researach postings and professors whose areas of study are the most relavent to their knowledge, skillset, and interests. It also allows for professor to see what students might be the most well-suited to provided aid on their research endeavors.

To build the recommendation system, we first had to decide what the structure of how a user - student or professor, and how a posting would be represented - what attributes we wanted to consider, etc. This portion of design was done in collaboration with the backend team, as they were chiefly maintaining the database to store these structures. Once the design of data storage was settled, we developed means of creating test data, such as writing a script for doing so. 

Following this, we needed to consider the existing framework regarding recommendation systems, and the pros and cons of various approaches. Eventually, we settled upon a method that, given some profile, would aim to find the profiles and postings that maximize a similarity metric, and return those as recommendations.

To accomplish this, we first needed to transform the profile/posting into a set of terms that best represent the profile/posting. This step can be referred to as key term extraction. Let us define a key term as a singular word or a set of multiple words grouped together that are important in the text they reside in. For this, we used the PyTextRank implementation of the TextRank algorithm. The algorithm itself is somewhat of analogue to the PageRank algorithm for websites. In the extractive version of this algorithm, a lemma graph is created to represent candidate phrases and their supporting language. Based on the finished state of this graph, the top phrases are returned.

 Once we have extracted key terms we need to consider the similarity of the sets themselves. Given a set of key phrases A, and a list of sets of other key terms, for each set B in the list, compare the similarity of B with A by taking the sum of the similarity score for each possible pair of phrases (a,b), a in A and b in B, and then normalize by dividing by the number of terms in set B:

 <img src="https://raw.githubusercontent.com/DSC-UIUC/rbay-data-ml/master/recommendation_scratch_space/sim_set_formula.png" alt="Logo">

However, we need a way to actually calculate the similarity between a pair of terms. This is where utilized the Gensim implementation of the Doc2Vec algorithm. On a high level, Doc2Vec aims to create a numeric model of text corpuses - it attempts to embed words into vectors, and paragraphs into vectors as well, in the Distributed Memory of Paragraph Vector implementation, which is what we are utilizing.  It is an unsupervised learning algorithm. Gensim provides an implementation of this algorithm and a multitude of handy functions we can use to call on models trained with their implementation. We called upon a function that computes the cosine similarity - the cosine of the angle between to vectors in the embedded space - between sets of words.

Of course, we need to text for the algorithm to train on. For this, we originally considered a data set that contained 250,000 computer science related research paper titles and abstracts. However, we found greater accuracy when we considered a model that was trained with the entire text of the English Wikipedia, a much larger dataset, so we selected to use that instead.
So, the entirety of the recommendation system is located in recommendations.py, where several events occur. There is a call made to Firebase Storage to download the model, and to Firestore to get the current postings and profiles. Key term extraction is performed on each of these postings and profiles. Then, we take the set of students and postings and perform our classification algorithm as described on each posting for each student, and return the top postings for each student. This is repeated for professors to students as well, and then students to professors. Finally, these recommendations are converted into a smaller representation and then written to a collection in the database.

As stated, the entirety of the recommendation generation is located in recommendations.py. You can run this script locally by simply calling
```bash
python recommendations.py
```
Note Python 3 is required.

This version of the script downloads the model from Firebase Storage, which will take some time depending on the strength of your connection. If you want this to run much more quickly, you may wish to download the model to your local storage, and uncomment the line in main() that reads the model path in from your local storage. Additionally, the default number of recommendations generated is 3, but that can be changed simply by changing the value of num_recs in main().

Here is a summary of the important functions in recommendations.py:

* main() - Runs the program by calling the supplementary functions
* get_model() - Downloads the Wikipedia-based model from storage (note the supplementary NumPy array files are required to be downloaded and present in the same directory as the model binary file itself)
* get_postings() - returns the posting data from Firestore
* get_students_and_professors() - returns the student and professor profile data from Firestore
* keyword_extract() - collects the key terms from the profiles and postings (we considered coursework, skills, and research interests to already be in form to be considerd key terms themselves)
* gen_keyword_extract() - uses PyTextRank to collect the key terms out of the freeform text in profiles and postings, called from keyword_extract()
* req_check() - checks to make sure all requirements a posting has are fulfilled by the student, if they aren't then that posting will simply be skipped from finding a similarity score, and has no chance of being recommended at all.
* classify() - the main classifcation function that takes in the list of key term sets and returns the list of the top (num_recs) posting/profile key term sets for the given student/professor key term set - for all students/professors in the database. This uses Gensim's n_similarity() function for finding the similarity between terms.
* write_recs() - converts the key term sets into the IDs of the profiles/postings they correspond to, then writes each set of recommended IDs to the database, with the document ID being the ID of the student/professor who the recommendations are for.

Here are the citations to the papers for where to look for the Wikipedia-trained model, and Doc2Vec itself:

Jey Han Lau and Timothy Baldwin (2016). An Empirical Evaluation of doc2vec with Practical Insights into Document Embedding Generation. In Proceedings of the 1st Workshop on Representation Learning for NLP, 2016.

Quoc Le and Tomas Mikolov (2014). Distributed Representations of Sentences and Documents. In Proceedings of the 31st International Conference on International Conference on Machine Learning, 2014.

Finally, here is a look at what the recommendations look like to the user:
<img src="https://raw.githubusercontent.com/DSC-UIUC/rbay-data-ml/master/recommendation_scratch_space/rec-example.png" alt="Logo">


#### Additional Scripts

The data_uploading_scripts directory provides one means of generating profiles. Data was collected by using a list of technical skills available on LinkedIn, scraping through LinkedIn bios to generate bios, a list of majors available at the University of Illinois, and some arbitrary names.
StudentProfile.py generates the profile object itself by selecting from the data, and data_to_base.py calls on profile creation and then writes the profiles to the database. The shell script data_to_base.sh exists to circumvent an error arising from attempting to write multiple profiles to Firestore from data_to_base.py.

create_model.py provides a means of generating a Doc2Vec model using Gensim. It reads in a text file with a cleaned dataset - stop words removed, etc.
It then trains on this dataset to create a model file. The hyperparameters in train_model() can be adjusted for various levels of desired performance.


