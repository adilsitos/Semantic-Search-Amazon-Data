# Semantic-Search-Amazon-Data

This repository contains the experiments to create the embeddings of book descriptions from the Book metadata that is part of the [Amazon Review dataset](https://nijianmo.github.io/amazon/index.html)(Jianmo Ni, Jiacheng Li, Julian McAuley. Empirical Methods in Natural Language Processing (EMNLP), 2019). The project was completed as part of the [Queensland AI](https://www.qldaihub.com/) fastai Community Course.

The user interface was built with [Streamlit](https://streamlit.io/) and is currently on in: [Semantic Search based on metadata](https://share.streamlit.io/adilsitos/semantic-search-amazon-data/main/ui.py).

The application takes a short description as an input from the user, and returns the titles of the most relevant books, based on their similarity score. The application can use one of two models: an AWD-LSTM which can be used with fastai, or a [sentence transformer](https://www.sbert.net/) from Hugging Face.

A diagram that explains how the application works can be found [here](https://whimsical.com/semantic-search-project-Mh4EHeCzX58fXZVYfFn4T1).
