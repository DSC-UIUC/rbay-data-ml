<style TYPE="text/css">
code.has-jax {font: inherit; font-size: 100%; background: inherit; border: inherit;}
</style>
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
    tex2jax: {
        inlineMath: [['$','$'], ['\\(','\\)']],
        skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'] // removed 'code' entry
    }
});
MathJax.Hub.Queue(function() {
    var all = MathJax.Hub.getAllJax(), i;
    for(i = 0; i < all.length; i += 1) {
        all[i].SourceElement().parentNode.className += ' has-jax';
    }
});
</script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-AMS_HTML-full"></script>

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

* [Firebase-Admin](https://firebase.google.com)
* [Google-Cloud](https://cloud.google.com)

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

TODO description, brief technical overview/details, screenshot(s) of relevant pages

#### Recommendation System

The recommendation system provides a way to be able to allow students to see researach postings and professors whose areas of study are the most relavent to their knowledge, skillset, and interests. It also allows for professor to see what students might be the most well-suited to provided aid on their research endeavors.

To build the recommendation system, we first had to decide what the structure of how a user - student or professor, and how a posting would be represented - what attributes we wanted to consider, etc. This portion of design was done in collaboration with the backend team, as they were chiefly maintaining the database to store these structures. Once the design of data storage was settled, we developed means of creating test data, such as writing a script for doing so. 

Following this, we needed to consider the existing framework regarding recommendation systems, and the pros and cons of various approaches. Eventually, we settled upon a method that, given some profile, would aim to find the profiles and postings that maximize a similarity metric, and return those as recommendations.

To accomplish this, we first needed to transform the profile/posting into a set of terms that best represent the profile/posting. This step can be referred to as key term extraction. Let us define a key term as a singular word or a set of multiple words grouped together that are important in the text they reside in. For this, we used the PyTextRank implementation of the TextRank algorithm. The algorithm itself is somewhat of analogue to the PageRank algorithm for websites. In the extractive version of this algorithm, a lemma graph is created to represent candidate phrases and their supporting language. Based on the finished state of this graph, the top phrases are returned.

 Once we have extracted key terms we need to consider the similarity of the sets themselves. Given a set of key phrases A, and a list of sets of other key terms, for each set B in the list, compare the similarity of B with A by taking the sum of the similarity score for each possible pair of phrases (a,b), a in A and b in B, and then normalize by dividing by the number of terms in set B:

 $sim(A,B) = \frac{\sum_{a \in A} \sum_{b \in B} sim(a,b)}{|B|}$

However, we need a way to actually calculate the similarity between a pair of terms. This is where utilized the Gensim implementation of the Doc2Vec algorithm. On a high level, Doc2Vec aims to create a numeric model of text corpuses - it attempts to embed words into vectors, and paragraphs into vectors as well, in the Distributed Memory of Paragraph Vector implementation, which is what we are utilizing.  It is an unsupervised learning algorithm. Gensim provides an implementation of this algorithm and a multitude of handy functions we can use to call on models trained with their implementation. We called upon a function that computes the cosine similarity - the cosine of the angle between to vectors in the embedded space - between sets of words.

Of course, we need to text for the algorithm to train on. For this, we originally considered a data set that contained 250,000 computer science related research paper titles and abstracts. However, we found greater accuracy when we considered a model that was trained with the entire text of the English Wikipedia, a much larger dataset, so we selected to use that instead.
So, the entirety of the recommendation system is located in recommendations.py, where several events occur. There is a call made to Firebase Storage to download the model, and to Firestore to get the current postings and profiles. Key term extraction is performed on each of these postings and profiles. Then, we take the set of students and postings and perform our classification algorithm as described on each posting for each student, and return the top postings for each student. This is repeated for professors to students as well, and then students to professors. Finally, these recommendations are converted into a smaller representation and then written to a collection in the database.

#### Additional Scripts

