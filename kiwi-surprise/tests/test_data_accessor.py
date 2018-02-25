from asynctest import TestCase, MagicMock, ANY, CoroutineMock 
from kiwi.TransferTypes import Vote
from kiwi.database.DataAccessor import DataAccessor
from pandas import DataFrame
from surprise import Dataset
from aiomysql import Connection, Cursor


class DataAccessorTest:

    def setUp(self):
        connection = MagicMock(spec=Connection)
        cursor = MagicMock(spec=Cursor)
        connection.cursor.return_value = cursor
        cursor.__aenter__ = CoroutineMock(return_value=cursor)
        cursor.fetchmany = CoroutineMock()

        self.accessor = DataAccessor(connection)
        self.connection = connection
        self.cursor = cursor
