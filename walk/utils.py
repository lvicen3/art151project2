import pickle as pkl
import re


# Function to split a document into a list of tokens
# Arguments:
# doc: A string containing input document
# Returns: tokens (list)
# Where, tokens (list) is a list of tokens that the document is split into
def get_tokens(doc):
	tokens = re.split(r"[^A-Za-z0-9-']", doc)
	tokens = list(filter(len, tokens))
	return tokens


# Function to split a document into a list of tokens
# Arguments: None
# Returns: stopwords (set)
# Where, stopwords (set) is a list of stopwords to be filtered from the document
def get_stopwords():
    stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
                    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
                    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
                    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
                    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
                    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
                    'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
                    'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
                    'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
                    'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
                    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
                    'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
                    "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren',
                    "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn',
                    "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't",
                    'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",
                    'won', "won't", 'wouldn', "wouldn't"])
    return stopwords



# Function to load word vectors pre-trained on Google News
# Arguments: None
# Returns: w2v (dict)
# Where, w2v (dict) is a dictionary with words as keys (lowercase) and vectors as values
def load_w2v():
    with open('w2v.pkl', 'rb') as fin:
        return pkl.load(fin)