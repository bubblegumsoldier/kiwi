import pandas as pd
import numpy as np
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize


class ContentEngine:

    def __init__(self, content, ratings, user_vectors=None):
        """
        :ratings:       Pandas dataframe with User, ItemId, Rating
        :content:       Pandas dataframe with ItemId Tags (tags as | separated                  substrings)
        :user_vectors:  Precalculated user taste vectors. Dataframe with index                  = UserId. Other columns are the feature vector elements.
        """
        self.ratings = ratings
        self.content = content
        self.user_vectors = user_vectors
    
    def fit(self):
        self.build_feature_vectors()
        if self.user_vectors is None:
            self.build_user_taste_vectors() 
        return self          

    def build_feature_vectors(self, content=None):
        """
        :content: Pandas dataframe with ItemId Tags (tags as | separated                  substrings). Uses the content instance variable if None
        """
        content = self.content if content is None else content

        start = time.time()
        self.tf_vectors = self._train_vectorizer(content)
        print("Engine trained in %s seconds." % (time.time() - start))

    def build_user_taste_vectors(self, ratings: pd.DataFrame=None):
        """
        User taste vectors for all users in the rating set.

        :ratings:   Dataframe with UserId, ItemId, Like where likes                         values 1 or -1. If None uses rating frame passed
                    in on creation.
        """
        ratings = self.ratings if ratings is None else ratings
        start = time.time()
        
        self.user_vectors = ratings \
            .groupby('UserId')['ItemId', 'Like'] \
            .apply(self._build_user_vector)   
        print('User training in {} seconds'.format(time.time() - start))

    def build_user_taste_vector(self, uid, ratings=None, insert=False):
        """
        Build user taste vector by summing the feature vectors of items he likes and subtracting item vectors he dislikes.

        :ratings: DataFrame with columns UserId, ItemId, Like where Like has values (-1, 1)
        :returns: Series with unnormalized user taste vector
        """
        ratings = self.ratings if ratings is None else ratings
        #normalize vector to unit length
        for_user = ratings[ratings['UserId'] == uid][['ItemId', 'Like']] 

        vector = self._build_user_vector(for_user)    
        if insert and self.user_vectors is not None:
            self.user_vectors.loc[uid] = vector.values
        return vector


    def predict_similarities(self, user, item=None):
        """
        Predicts items that are similar to the users tastes.

        :user: User id of the user in question
        :item: Item id of a item that should be estimated.
        :returns: Numpy array of [similarity, itemid]. (shape: n, 2). If item             != None returns similarity for this item.
        """
        if item is None:
            return self._predict_all(user)
        return self._predict_single(user, item)   
    

    def _train_vectorizer(self, ds):
        """
        Train the content engine.

        :param ds: Pandas dataset containing two columns: Tags & ItemId
                   Tags have to be of the form tag1|tag2|tag3
        """

        tf = TfidfVectorizer(analyzer='word',
                             ngram_range=(1, 1),
                             token_pattern='[^|]+',
                             min_df=0,
                             stop_words='english')
        tfidf_matrix = tf.fit_transform(ds['Tags'])
        self.feature_names = tf.get_feature_names()
        frame_id = pd.DataFrame(index=ds['ItemId'])
        frame_id['ItemId'] = frame_id.index
        frame_content = pd.DataFrame(tfidf_matrix.toarray(), index=ds['ItemId'])
        return frame_id.join(frame_content, how='inner')
        


    def _build_user_vector(self, for_user):
        #merge -> ItemId, Like, Features
        merged = for_user.merge(self.tf_vectors, how='inner', on='ItemId')
        _slice = merged.iloc[:, 2:].multiply(merged['Like'], axis=0).sum()
        series = pd.Series(_slice)
        return series


    def _predict_all(self, user):
        user_vector = self._get_user_vector(user)
        all_sims = cosine_similarity(
            user_vector.values.reshape(1,-1), 
            self.tf_vectors.iloc[:,1:]
            ).flatten()
        frame = pd.DataFrame(all_sims, columns=['Similarities'])
        frame['ItemId'] = self.content['ItemId']
        frame.sort_values(by='Similarities', ascending=False, inplace=True)
        return frame

    def _predict_single(self, user, item):
        user_vector = self._get_user_vector(user).values.reshape(1,-1)
        sim = cosine_similarity(
            user_vector, 
            self.tf_vectors[self.tf_vectors['ItemId'] == item].iloc[:,1:]
            ).flatten()
        return np.stack([sim, [item]],axis=1).flatten()
        

    def _get_user_vector(self, user):
        if self.user_vectors is not None:
            return self.user_vectors.loc[user]
        return self.build_user_taste_vector(user, insert=True)

