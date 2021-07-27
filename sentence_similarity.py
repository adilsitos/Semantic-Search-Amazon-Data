import json
import sys
import os
from collections import OrderedDict
import numpy as np
import pandas as pd
import time
from sklearn.decomposition import PCA
import torch
import pickle
import warnings
from torch import Tensor
import pandas as pd
from sentence_transformers import SentenceTransformer

from azureml.core.model import Model

MODEL_NAME = 'semantic-search'
MODEL_FILE_NAME = 'features_sentence_sim.pkl'

warnings.warn("deprecated", DeprecationWarning)

def init():
    """
    Init step: load the featurizer, model and PCA as global variables. Will be used in run step.
    """
    global feat_extract, pca_transformer, dat_lookup, model, sentence_encoder
    # Load features and encoding
    model_dir = Model.get_model_path(MODEL_NAME)
    
    pickle_f = os.path.join(model_dir, MODEL_FILE_NAME)
    #with open(pickle_f, "rb") as pickle_file:
    pickle_content = pickle.load(open(model_dir, 'rb'))
    dat_lookup = pickle_content[0]
    feat_extract = pickle_content[1]
    pca_transformer = pickle_content[2]
    try:
        #Loading feature extractor
        sentence_encoder = SentenceTransformer('bert-base-nli-mean-tokens')
    except:
        raise Exception("Bad input: Unable to load pickle file from api ")
    print('init() done.')


def pytorch_cos_sim(a: Tensor, b: Tensor):
    """
    Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.
    :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
    """
    return cos_sim(a, b)

def cos_sim(a: Tensor, b: Tensor):
    """
    Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.
    :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
    """
    if not isinstance(a, torch.Tensor):
        a = torch.tensor(a)

    if not isinstance(b, torch.Tensor):
        b = torch.tensor(b)

    if len(a.shape) == 1:
        a = a.unsqueeze(0)

    if len(b.shape) == 1:
        b = b.unsqueeze(0)

    a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
    b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
    return torch.mm(a_norm, b_norm.transpose(0, 1))

def format_output(Filtered_dat):
    """
    Format outputs as a json.

    Parameters
    ----------
    Filtered_dat : dataframe to be converted to json
     """
    try:
        # Define a static order for json fields (for testing purposes)
        output_json = {}
        #keyorder = ['title', 'description', 'score']

        # Concatenate boxes, scores and classes in one dataframe
        df = Filtered_dat

        output_json = df.to_json()

        return output_json
    except:
        raise Exception("Bad format: Unable to format outputs with the predefined json structure.")


def feature_extractor(x):
    """
        Convert a the search string into feature array and send it back

        Parameters
        ----------
        x : search string.
            
        """
    feat = sentence_encoder.encode(x)
    feat = (np.array(feat)).reshape(1, -1) 
    return feat

def pcatransformer(x):
    return pca_transformer.transform(x)

def similar_search(pca_feat):
    """
        Takes the pca extracted features of the embedding 
        and finds similar items using cosine distance
        Parameters
        ----------
        pca_feat : Embedding transformed by pca
        ranks_return: number of ranks to be returned
        """
    similarity_score_torch = pytorch_cos_sim(
                        feat_extract,
                        pca_feat
                    )
    # Taking top 10 sentences
    topK_scores = torch.topk(similarity_score_torch, 10, dim=0)
    # Storing the score for top 3 titles
    result = dat_lookup.iloc[topK_scores[1].squeeze().tolist()]
    result['scores']=topK_scores[0].squeeze().tolist()
    return result

def run(input_json):
    """
    Run Search string. Returns result in the API expected format.
    This is the entrypoint for API calls.

    Parameters
    ----------
    input_json : Search string.
        Json dumps that contains input search string and parameters.
    """
    input_dict = json.loads(input_json)
    search_string = input_dict["search_string"]
    ID = input_dict["ID"]
    
    try:
        # run feature extractor
        x = search_string
        feat = feature_extractor(x)

        #run PCA transformer
        pca_feat = pcatransformer(feat)

        # Get top 10 similar books
        ranked_dat = similar_search(pca_feat)

        # Format outputs
        output_json = format_output(ranked_dat)
        
        # Concatenate inputs and outputs to be sent out
        output_dict =input_dict
        output_dict['response'] = output_json
        
        return output_dict

    except Exception as e:
        input_dict['response'] = str(e)
        results = {'code': 1, 'error_msg': str(e)}
        return results