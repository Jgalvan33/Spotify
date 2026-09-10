from cassandra.cluster import Cluster
import uuid

# Conectarse al cluster
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
print("Conectado a Cassandra Cluster")

# Crear el Keyspace

CREATE_KEYSPACE = """
CREATE KEYSPACE IF NOT EXISTS spotify
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
"""

session.execute(CREATE_KEYSPACE)
session.set_keyspace("spotify")
print("Keyspace spotify seleccionado")

# Crear tabla
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS spotify_songs (
album TEXT, release_year INT,
song_name TEXT, artist TEXT,
song_id UUID,
PRIMARY KEY (album, release_year, song_name)
)
"""
stmt = session.prepare(CREATE_TABLE)
session.execute(stmt)
print("Tabla creada")

# Modificar tabla
ALTER_TABLE_RATING = """
ALTER TABLE spotify_songs ADD rating FLOAT
"""
ALTER_TABLE_GENRE = """
ALTER TABLE spotify_songs ADD genre TEXT
"""
session.execute(ALTER_TABLE_RATING)
session.execute(ALTER_TABLE_GENRE)
print("Tabla modificada")

# Insertar una canción
INSERT_SONG = """
INSERT INTO spotify_songs
    (album, release_year, song_name, 
    artist, rating, genre, song_id)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""
song_id = uuid.uuid4()
stmt = session.prepare(INSERT_SONG)
session.execute(stmt, ("Greatest_Hits", 2022, 
                       "Song_1", "The Cdodes", 4.5, "Pop", song_id))

print("Canción insertada")
# Consultar datos

SELECT_ALL = "SELECT * FROM spotify_songs"

stmt = session.prepare(SELECT_ALL)
rows = session.execute(stmt)

for r in rows:
    print(r.album, r.release_year, r.song_name, r.artist, r.rating, r.genre)

# Actualizar datos
UPDATE_RATING = """
UPDATE spotify_songs
SET rating=?
WHERE album=? AND release_year=?
  AND song_name=?
"""
stmt = session.prepare(UPDATE_RATING)
session.execute(stmt, (5.0, "Greatest Hits",
  2022, "Song_1"))

print("Dato actualizado")

# Eliminar datos
DELETE_BY_RATING = """
DELETE FROM spotify_songs
WHERE album=? AND release_year=?
  AND song_name=?
"""

stmt = session.prepare(DELETE_BY_RATING)
session.execute(stmt, ("Greatest Hits",
  2022, "Song_1"))
print("Dato eliminado")

# Eliminar tabla y cerrar sesión
DROP_TABLE = """DROP TABLE IF EXISTS spotify_songs"""
stmt = session.prepare(DROP_TABLE)
session.execute(stmt)

cluster.shutdown()
print("Sesión finalizada")
