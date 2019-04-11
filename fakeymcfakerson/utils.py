from sqlalchemy.dialects.postgresql.base import (
    UUID,
)
from sqlalchemy.sql.sqltypes import (
    BIGINT,
    BigInteger,
    CHAR,
    DATE,
    DATETIME,
    DECIMAL,
    Date,
    DateTime,
    FLOAT,
    Float,
    INT,
    INTEGER,
    Integer,
    NCHAR,
    NUMERIC,
    NVARCHAR,
    Numeric,
    REAL,
    SMALLINT,
    SmallInteger,
    TIME,
    TIMESTAMP,
    VARCHAR,
)

integer_types = [
    BIGINT,
    BigInteger,
    INT,
    INTEGER,
    Integer,
    SMALLINT,
    SmallInteger,
]

date_types = [
    DATE,
    DATETIME,
    Date,
    DateTime,
    TIME,
    TIMESTAMP,
]

float_types = [
    DECIMAL,
    FLOAT,
    Float,
    NUMERIC,
    Numeric,
    REAL,
]

min_max_types = integer_types + date_types + float_types

distinct_types = [
    CHAR,
    NCHAR,
    NVARCHAR,
    VARCHAR,
]

id_types = [
    UUID
]


class DoNotUse(object):
    def __repr__(self):
        return 'DoNotUse'


LOREM_IPSUM = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut egestas tellus in lectus mollis ultricies. Suspendisse 
volutpat elit sit amet nulla gravida sollicitudin. Etiam egestas dolor nisl, et pellentesque tortor convallis nec.
 Donec finibus tellus enim, sed porttitor tortor gravida vel. In hac habitasse platea dictumst. Pellentesque odio nibh, 
 scelerisque a eleifend non, mattis et sapien. Praesent laoreet justo felis. Aenean interdum turpis suscipit nisl 
 vestibulum, semper pretium mi porttitor.

Ut vitae magna ac lacus scelerisque condimentum sed eu odio. Etiam posuere rutrum turpis, et porttitor arcu semper eget.
 Proin non elit nec quam eleifend vulputate non nec dui. Vivamus nec nibh vitae sapien fermentum dapibus. Fusce vehicula
  quam est, id euismod dui iaculis vitae. Nam tincidunt lacus in purus ultricies dignissim. Donec eu tortor a magna 
  sodales blandit. Phasellus accumsan dolor pretium leo feugiat iaculis. Quisque nec sem dui.

Praesent non est eget neque dignissim aliquet. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere 
cubilia Curae; Nulla egestas, nisl sodales varius consectetur, odio leo faucibus enim, et commodo nunc dui at mi. 
Nullam ullamcorper justo eget dictum aliquet. Donec et finibus tortor. Nunc lacus nulla, tristique non maximus 
vestibulum, luctus id sapien. Praesent in mauris rutrum, mollis ante vel, cursus nulla. Phasellus est purus, commodo 
interdum leo id, dictum efficitur neque. Ut tortor orci, sollicitudin a dui id, consectetur pellentesque lacus. In 
vitae sollicitudin libero, at maximus augue. Nullam hendrerit fringilla augue id rhoncus. Sed tincidunt pharetra tempus.

Aliquam ex diam, tincidunt eu volutpat sit amet, porta eu justo. Pellentesque blandit porttitor metus, vulputate 
fringilla lectus malesuada at. Cras id erat sed libero pulvinar lobortis nec ut turpis. Proin ultricies laoreet 
molestie. Aliquam sed sem sed elit vulputate malesuada ac in nisi. Vestibulum ante ipsum primis in faucibus orci luctus 
et ultrices posuere cubilia Curae; Pellentesque eu congue nulla, vel tempor tortor. Curabitur ac tortor varius, placerat
 nunc eu, fringilla nunc. Nunc sit amet enim dignissim, porta sapien id, dictum eros. Duis dignissim lacus sed purus 
 tempor, at porttitor turpis bibendum. Donec ac tempus velit. Pellentesque mollis sollicitudin lorem ut auctor. 
 Phasellus accumsan arcu tortor, tempus facilisis nisl rutrum consequat. Curabitur eget ex lorem.

Fusce sollicitudin lacus sed nulla sagittis tempus. Mauris in dui et tortor consequat varius. Maecenas dolor purus, 
convallis ut tincidunt non, gravida non ligula. Suspendisse potenti. Praesent congue porttitor sapien at pulvinar. 
Praesent eros lorem, lobortis quis tellus id, gravida lacinia erat. Quisque bibendum urna vitae lectus condimentum, 
quis sagittis ipsum fringilla. Sed malesuada risus mi, ut laoreet justo blandit eu.
"""
