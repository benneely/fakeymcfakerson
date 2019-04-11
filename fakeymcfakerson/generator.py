import numpy as np
from fakeymcfakerson.utils import *
import pickle
from sqlalchemy import create_engine
import uuid
import random
import string
import datetime
from random import randrange
from sqlalchemy.engine import Engine
from sqlalchemy import event
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlite3 import Connection as SQLite3Connection

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


class Generator():
    def __init__(
            self,
            reflection_database_connect_string=None,
            config_file='./fakeymcfakerson_metadata.p',
    ):
        """
        Class responsible for generating fake data
        :param connect_object: fakeymcfakerson.connect.Connect object
        :param config_file: str: place where configuration file is stashed
        """
        self.engine = create_engine(reflection_database_connect_string)
        try:
            self.config_file = config_file
            self.metadata = self.import_metadata_pickle()
            OriginSessionMaker = sessionmaker(bind=self.engine)
            self.session = OriginSessionMaker()
            conn = self.engine.connect()
            self.metadata['sqlalchemy_metadata'].create_all(self.engine)
        except Exception as e:
            print(e)

    def import_metadata_pickle(self):
        with open(self.config_file, 'rb') as f:
            results = pickle.load(f)
        return results

    def _query_table_dot_column_return_unique_values(self, dot_name):
        table, column = dot_name.split('.')
        related_table = [tbl for tbl in self.metadata['sqlalchemy_metadata'].sorted_tables if tbl.name == table][0]
        related_column = [col for col in list(related_table.columns) if col.name == column][0]
        r = self.session.query(related_column).distinct()
        result = [a[0] for a in r]
        return result


    def generate_fake_table_and_insert(self, table, sample_size=10):
        tbl_metadata = self.metadata['column_metadata'][table.name]
        primary_key_cols = [x.name for x in list(table.primary_key)]
        foreign_key_cols = [item for sublist in
                            [list(col.columns )for col in [fk for fk in list(table.foreign_key_constraints)]] for item
                            in sublist]
        results = {}
        for col in tbl_metadata:
            if col['col_name'] in [fk.name for fk in  foreign_key_cols]:
                indx = [i for i, fk in enumerate(foreign_key_cols) if col['col_name']==fk.name][0]
                related_table_dot_name = list(foreign_key_cols[indx].foreign_keys)[0].target_fullname
                related_choices = self._query_table_dot_column_return_unique_values(related_table_dot_name)
                results[col['col_name']] = generate(col, sample_size, foreign_key=True, forced_column_choices=related_choices)
            elif col['col_name'] in primary_key_cols:
                results[col['col_name']] = generate(col, sample_size, unique=True)
            else:
                results[col['col_name']] = generate(col, sample_size)
        final = [dict(zip(results,t)) for t in zip(*results.values())]
        connection = self.engine.connect()
        #TODO: find a way to use core, right now trying to insert final fails, but inserting an unamed list works?
        # connection.execute(table_object.insert(), final)
        df = pd.DataFrame(final)
        df.to_sql(table.name, connection, if_exists='append', index=False)
        connection.close()
        print('Generated ' + str(sample_size) + ' records for table: ' + table.name)
        return results

    def generate_all_tables(self):
        for tbl in self.metadata['sqlalchemy_metadata'].sorted_tables:
            try:
                self.generate_fake_table_and_insert(
                    tbl,
                    sample_size=self.metadata['table_metadata'][tbl.name]
                )
            except:
                raise Exception


def generate(col, sample_size, unique=False, foreign_key=False, forced_column_choices=None):
    assert isinstance(col, dict), 'generate only accept dictionaries from fakeymcfakerson pickle files.'
    if foreign_key:
        choices = forced_column_choices
        anonymous=False
        col['col_type'] = distinct_types[0]()
    elif isinstance(col['col_values'][0], DoNotUse):
        anonymous=True
        choices = []
    else:
        anonymous=False
        choices=col['col_values']
    if isinstance(col['col_type'], tuple(id_types)):
        return uuid_generator(sample_size)
    elif isinstance(col['col_type'], tuple(distinct_types)):
        return distinct_generator(
            choices,
            col['col_type'].length,
            sample_size, unique,
            anonymous
        )
    elif isinstance(col['col_type'], tuple(integer_types)):
        return min_max_generator_integer(
            choices,
            sample_size,
            unique,
            anonymous
        )
    elif isinstance(col['col_type'], tuple(float_types)):
        return min_max_generator_float(
            choices,
            sample_size,
            unique
        )
    elif isinstance(col['col_type'], tuple(date_types)):
        return min_max_generator_date(
            choices,
            sample_size
        )


def min_max_generator_date(min_max_list, sample_size):
    """
    Given a list of [min, max] will randomly generate (n=sample_size) many
    :param min_max_list: list of length 2 [min date, max date]
    :param sample_size: length of the sample to return
    :return: list of length sample_size
    """
    start = min_max_list[0]
    end = min_max_list[1]
    delta = end - start
    return [start+datetime.timedelta(days=randrange(delta.days)) for i in range(sample_size)]


def min_max_generator_float(min_max_list, sample_size, anonymous=True):
    """
    Given a list of [min, max] will randomly generate (n=sample_size) many
    :param min_max_list: list of length 2 [min, max]
    :param sample_size: length of the sample size to return
    :return: list of length sample_size
    """
    if anonymous:
        return list(np.random.uniform(0, 1, sample_size))
    else:
        return list(np.random.uniform(min_max_list[0], min_max_list[1], sample_size))


def min_max_generator_integer(min_max_list, sample_size, unique=False, anonymous=True):
    """
    Given a list of [min, max] will randomly generate (n=sample_size) many
    :param min_max_list: list of length 2 [min, max]
    :param sample_size: length of the sample size to return
    :return: list of length sample_size
    """
    if anonymous:
        if unique:
            return [x for x in range(sample_size)]
        else:
            return list(np.random.random_integers(0, 100, sample_size))
    else:
        if unique:
            return [x for x in range(sample_size)]
        else:
            return list(np.random.random_integers(min_max_list[0], min_max_list[1], sample_size))


def distinct_generator(choice, len, sample_size, unique=False, anonymous=True):
    """
    Given a list of [unique values] will randomly generate (n=sample_size) many
    :param choice: list of length n unique values
    :param type: one of the classes listed in fakeymcfakerson.utils
    :param sample_size: length of the sample size to return
    :param fromrandom: bool, to use metadata or not to generate data
    :return: list of length sample_size
    """
    if anonymous:
        if unique:
            return [uuid.uuid4().hex[:len] for x in range(sample_size)]
        else:
            return [''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(len))
                    for x in range(sample_size)]
    else:
        return list(np.random.choice(choice, sample_size))


def uuid_generator(sample_size):
    """
    Given a list of [unique values] will randomly generate (n=sample_size) many
    :param type: one of the classes listed in fakeymcfakerson.utils
    :param sample_size: length of the sample size to return
    :return: list of length sample_size
    """
    return [str(uuid.uuid4()) for i in range(sample_size)]
