# fakeymcfakerson
A python package that uses sqlalchemy reflect to stand up a development server /
schema based on real data. Several mechanism for data generation will be explored.

![](repo_imgs/project.gif)

## Usage
First, we require users to create an intermediate python pickle object which acts as a configuration
for data generation. This is accomplished via the `fakeymcfakerson.reflect.Reflect` class. Here is
example usage using `sqlite`. The `ehr.db` database referenced can be generated via the `scripts` 
folder.
```
from fakeymcfakerson.reflect import Reflect

reflection = Reflect(
    origin_database_connect_string='sqlite:///ehr.db',
    filter_column_name=['patient.id', 'Patient.name'],
    filter_table_name=['sqlite_master'],
    config_file='ehr.p'
    )

reflection.export_metadata_pickle()
```
**Note** the reflection class provides the following parameters: 
- `origin_database_connect_string`: A valid [sqlalchemy engine string](http://docs.sqlalchemy.org/en/latest/core/engines.html)
- `filter_column_name`: do not use actual data from db to generate fake data (e.g. MRN)
- `filter_table_name`: do not store or use these tables in generation (e.g. Django authentication tables)
- `config_file`: the full unc path and name of the pickled configuration object

Once the configuration file is in place, we can generate a new database with fake data via the `fakeymcfakerson.generators.Generator`
class. Here is example usage:

```
from fakeymcfakerson.generators import Generator

generator = Generator(
    reflection_database_connect_string='sqlite:///ehr_copy.db',
    config_file='ehr.p'
    )
    
e = generator.generate_all_tables()
```
**Note** the generator class provides the following parameters:
- `reflection_database_connect_string`: A valid [sqlalchemy engine string](http://docs.sqlalchemy.org/en/latest/core/engines.html)
where fake data tables will be written
- `config_file` - a python pickled object generated from `fakeymcfakerson.reflect.Reflect.export_metadata_pickle`

## Design Decision
The decision to utilize a configuration file stems from a desire to write plugins for data generation. Currently, the data
generation mechanism is very naive. It essentially independently and uniformly selects values from a know distribution without
incorporating any type of correlation (either between columns nor within patients/foreign key relationships).

## Known Issues
- Only tested on `sqlite`
- Configuration File is generated in memory - this will be a problem for large schemas
- Effeciency is dependent upon origin database setup. We expect data to be stored in appropriate types in the 
originating database (e.g. numeric data to be stored INT, dates to be stored as DATE). This will
facilitate the best generation.
