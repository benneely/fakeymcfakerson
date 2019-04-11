from fakeymcfakerson.utils import min_max_types, distinct_types, id_types, DoNotUse
from sqlalchemy import func
from fakeymcfakerson.utils import min_max_types, distinct_types
import pickle
from sqlalchemy import create_engine
import os
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm


class Reflect():
    def __init__(
            self,
            origin_database_connect_string,
            filter_column_name=None,
            filter_table_name=None,
            config_file='./fakeymcfakerson_metadata.p'):
        """
        Reflect is a class responsible for reflecting the database and generating a config file used by
        fakeymcfakerson.generators.Generator.
        :param origin_database_connect_string: str: engine text
        :param filter_column_name: list containing text of table.column to remove from configuration
        :param filter_table_name: list containing text of tables to exclude from configuration
        :param config_file: str: place to stash database config file, may contain sensitive information!
        """
        self.engine = create_engine(origin_database_connect_string)
        OriginSessionMaker = sessionmaker(bind=self.engine)
        self.session = OriginSessionMaker()

        self.origin_metadata = MetaData()
        print('Reflecting database...')
        self.origin_metadata.reflect(bind=self.engine)
        self.filter_column_name = [x.lower() for x in filter_column_name]
        table_names = [x for x in self.origin_metadata.tables]
        exclusion_table_names = [x.lower() for x in filter_table_name]
        self.only_tables = [x for x in table_names if x not in exclusion_table_names]
        self.origin_tables = [self.origin_metadata.tables.get(x) for x in self.only_tables]

        self.config_file = config_file
        self.metadata = self.generate_metadata()

    def get_unique_col_values(self, col):
        session = self.session
        return [x[0] for x in session.query(col.distinct())]

    def get_min_max_col_values(self, col):
        session = self.session
        return [x for x in session.query(func.min(col), func.max(col))[0]]

    def get_column_names(self, tbl):
        tbl_columns = []
        for col in tqdm(tbl.columns.values()):
            output = {}
            output['col_type'] = col.type
            output['col_name'] = col.name
            if tbl.name + '.' + col.name in self.filter_column_name:
                output['col_values'] = [DoNotUse()]
            else:
                if isinstance(col.type, tuple(min_max_types)):
                    output['col_values'] = self.get_min_max_col_values(col)
                elif isinstance(col.type, tuple(distinct_types)):
                    output['col_values'] = self.get_unique_col_values(col)
                elif isinstance(col.type, tuple(id_types)):
                    output['col_values'] = [DoNotUse()]
                else:
                    raise ValueError('fakeymcfakerson does not currently support types: ' +
                                     str(col.type) +
                                     '. Please create a Pull Request to allow for this type.')
            tbl_columns.append(output)
        return tbl_columns

    def generate_metadata(self):
        session = self.session
        column_metadata = {}
        table_metadata = {}
        for tbl in self.origin_tables:
            print('\nReflecting Table: ' + tbl.name)
            column_metadata[tbl.name] = self.get_column_names(tbl)
            table_metadata[tbl.name] = session.query(tbl).count()
        metadata = {
            'column_metadata': column_metadata,
            'table_metadata': table_metadata,
            'sqlalchemy_metadata': self.origin_metadata}
        return metadata

    def export_metadata_pickle(self):
        with open(self.config_file, 'wb') as f:
            pickle.dump(self.metadata, f)
        print('Saved metadata at ', os.path.abspath(self.config_file))
