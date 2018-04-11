from unittest import TestCase
from kiwi.ContentEngine import ContentEngine
import pandas as pd
from kiwi.TransferTypes import Vote


class ContentEngineTest(TestCase):
    def setUp(self):
        self.empty_content_frame = pd.DataFrame([], columns=['ItemId', 'Tags'])
        self.empty_ratings_frame = pd.DataFrame(
            [], columns=['UserId', 'ItemId', 'Like'])
        self.full_content_frame = pd.DataFrame.from_records(
            [('i1', 'Action|Comedy'), ('i2', 'Action|Adventure')], columns=['ItemId', 'Tags'])

        self.full_rating_frame = pd.DataFrame.from_records(
            [('u1', 'i1', 1), ('u2', 'i1', -1)], columns=['UserId', 'ItemId', 'Like'])

    def test_empty_setup_does_not_train(self):
        engine = ContentEngine(
            self.empty_content_frame,
            self.empty_ratings_frame)

        with self.assertRaises(ValueError):
            engine.fit()
            
        self.assertIsNone(engine.tf_vectors)
        self.assertIsNone(engine.user_vectors)

    def test_empty_setup_with_content(self):
        engine = ContentEngine(
            self.full_content_frame,
            self.empty_ratings_frame)

        engine.fit()
        self.assertFalse(engine.tf_vectors.empty)
        self.assertTrue(engine.user_vectors.empty)
        columns = engine.user_vectors.columns
        index = engine.user_vectors.index
        self.assertTrue(all(columns.contains(x) for x in [0, 1, 2]))
        self.assertTrue(index.empty)

    def test_empty_initial_ratings_rating_added(self):
        engine = ContentEngine(
            self.full_content_frame,
            self.empty_ratings_frame)

        engine.fit()
        engine.update_ratings(Vote(user='u1', post='1', vote=1))
        engine.build_user_taste_vector('u1', insert=True)
        self.assertEqual(engine.user_vectors.shape, (1, 3))

    def test_existing_taste_vector_does_not_change_without_update(self):
        engine = ContentEngine(
            self.full_content_frame,
            self.full_rating_frame)

        engine.fit()
        # engine.update_ratings(('u1', 'i2', 1))
        vector1 = engine.user_vectors.loc['u1']
        vector2 = engine.build_user_taste_vector('u1')
        self.assertEqual(vector1.tolist(), vector2.tolist())

    def test_update_existing_taste_vector(self):
        engine = ContentEngine(
            self.full_content_frame,
            self.full_rating_frame)

        engine.fit()
        engine.update_ratings(('u1', 'i2', 1))
        vector1 = engine.user_vectors.loc['u1'].tolist()
        vector2 = engine.build_user_taste_vector('u1', insert=True)
        inserted = engine.user_vectors.loc['u1']
        self.assertNotEqual(vector1, vector2.tolist())
        self.assertEqual(vector2.tolist(), inserted.tolist())

    def test_get_nonexisting_user_vector_raises(self):
        engine = ContentEngine(
            self.full_content_frame,
            self.full_rating_frame)

        engine.fit()
        with self.assertRaises(KeyError):
            engine.user_vectors.loc['u3']