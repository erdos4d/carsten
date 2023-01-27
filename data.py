from os import getenv
from traceback import print_exc

from dotenv import load_dotenv
from sqlalchemy import Table, Column, MetaData, BigInteger, Identity, String, Boolean, text, BLOB
from sqlalchemy.engine import create_engine

load_dotenv()
metadata = MetaData()
engine = create_engine(
    'postgresql://{}:{}@{}:{}/{}'.format(
        getenv('DB_USER'),
        getenv('DB_PASS'),
        getenv('DB_HOST'),
        getenv('DB_PORT'),
        getenv('DB_NAME'),
    )
)
results = Table(
    "results",
    metadata,
    Column('id', BigInteger, Identity(start=1, cycle=True), primary_key=True, autoincrement=True),
    Column('n', BigInteger),
    Column('beta', String),
    Column('q', String),
    Column('Q', String),
    Column('Tau', String),
    Column('m', String),
    Column('W0', BLOB),
    Column('W1', BLOB),
    Column('N', String),
    Column('B', BLOB),
    Column('C', BLOB),
    Column('E', BLOB),
    Column('V', String),
    Column('L', BLOB),
    Column('G', BLOB),
    Column('basis_check', Boolean),
    Column('rank_check', Boolean),
    Column('S', BLOB),
    Column('T', BLOB),
    Column('psi', String),
    Column('D', String),
    Column('t1', String),
    Column('t2', String),
    Column('beta3', String),
    Column('B_seconds', BigInteger),
    Column('lll_seconds', BigInteger),
    Column('total_seconds', BigInteger)
)
metadata.create_all(engine)

get_next_n_query = text('''INSERT INTO results(n)
VALUES ((SELECT coalesce(max(results.n), 0) + 2 FROM results))
RETURNING n;''')

insert_data_query = text('''UPDATE results SET
"beta" = :beta,
"q" = :q,
"Q" = :Q,
"Tau" = :Tau,
"m" = :m,
"W0" = :W0,
"W1" = :W1,
"N" = :N,
"B" = :B,
"C" = :C,
"E" = :E,
"V" = :V,
"L" = :L,
"G" = :G,
"basis_check" = :basis_check,
"rank_check" = :rank_check,
"S" = :S,
"T" = :T,
"psi" = :psi,
"D" = :D,
"t1" = :t1,
"t2" = :t2,
"beta3" = :beta3,
"B_seconds" = :B_seconds,
"lll_seconds" = :lll_seconds,
"total_seconds" = :total_seconds
WHERE n = :n RETURNING n;
''')


def get_n() -> int:
    try:
        with engine.begin() as connection:
            return next(connection.execute(get_next_n_query))[0]
    except:
        print_exc()


def insert_output(output: dict) -> bool:
    try:
        with engine.begin() as connection:
            return int(output.get('n')) == int(next(connection.execute(insert_data_query, **output))[0])
    except:
        print_exc()
        return False
