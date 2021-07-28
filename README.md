# Semantic Search for Book Recommendations with Amazon Data

This repository contains the experiments to create the embeddings of book descriptions from the Book metadata that is part of the [Amazon Review dataset](https://nijianmo.github.io/amazon/index.html)(Jianmo Ni, Jiacheng Li, Julian McAuley. Empirical Methods in Natural Language Processing (EMNLP), 2019). The project was completed as part of the [Queensland AI](https://www.qldaihub.com/) fastai Community Course.

## Application

The user interface was built with [Streamlit](https://streamlit.io/) and is currently on in: [Semantic Search based on metadata](https://share.streamlit.io/adilsitos/semantic-search-amazon-data/main/ui.py).

The application takes a short description as an input from the user, and returns the titles of the most relevant books, based on their similarity score. The application can use one of two models: an AWD-LSTM which can be used with fastai, or a [sentence transformer](https://www.sbert.net/) from Hugging Face.

A diagram that explains how the application works can be found [here](https://whimsical.com/semantic-search-project-Mh4EHeCzX58fXZVYfFn4T1).

The user interface includes a user feedback feature, which allows a user to report whether the recommendations were relevant or not. This feedback and the recommendations that the user received are stored in a web service hosted on Heroku.

## Code

The [Semantic-Search_Search_with_fastai Notebook](https://github.com/Adilsitos/Semantic-Search-Amazon-Data/blob/main/Semantic_Search_with_fastai.ipynb) shows the process to obtain the embeddings from the 2,384,197 book descriptions that were used.[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1PIMtkozBnfeEvCuAQcHyTCQr7mYF3dLg?usp=sharing)

The code for the Streamlit interface can be found on [ui.py](https://github.com/Adilsitos/Semantic-Search-Amazon-Data/blob/main/ui.py).

The code related to the Azure ML web service is found in [sentence_similarity.py](https://github.com/Adilsitos/Semantic-Search-Amazon-Data/blob/main/sentence_similarity.py) and [sentence_similarity_service.py](https://github.com/Adilsitos/Semantic-Search-Amazon-Data/blob/main/sentence_similarity_service.py). 
