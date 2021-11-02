import sqlalchemy
login = input('Внесение данных по музыкальному магазину в базу данных. \n Введите логин: ')
password = input('Введите пароль: ')
database = input('Введите название базы: ')
address = 'postgresql://' + login + ':' + password + '@localhost:5432/' + database
engine = sqlalchemy.create_engine(address)
connection = engine.connect()

sel = connection.execute("""SELECT COUNT(genre_id), title_genre
FROM performers_ganre A
JOIN genre B
ON A.genre_id = B.id
GROUP BY b.title_genre 
ORDER BY COUNT(*) DESC;
""")
print('Название и год выхода альбомов, вышедших в 2018 году:\n', *sel, '\n')

sel = connection.execute("""SELECT COUNT(track_name), title_albums
FROM albums A
JOIN tracks B
ON A.id = B.albums_id 
WHERE year_of_release <= 2020 AND year_of_release >= 2015
GROUP BY a.title_albums
ORDER BY COUNT(b.track_name) DESC;
""")
print('количество треков, вошедших в альбомы 2015-2020 годов:\n', *sel, '\n')


sel = connection.execute("""SELECT title_albums, AVG(duration)
FROM albums A
JOIN tracks B
ON A.id = B.albums_id 
GROUP BY a.title_albums 
ORDER BY AVG(duration) DESC;
""")
print('средняя продолжительность треков по каждому альбому:\n', *sel, '\n')

sel = connection.execute("""SELECT name_performers
FROM performers A
JOIN performers_albums B ON A.id = B.performers_id
JOIN albums C ON B.albums_id = C.id
WHERE A.name_performers NOT IN (
    SELECT name_performers
    FROM performers A
    JOIN performers_albums B ON A.id = B.performers_id
    JOIN albums C ON B.albums_id = C.id
    WHERE C.year_of_release = 2020)
GROUP BY A.name_performers;
""")
print('все исполнители, которые не выпустили альбомы в 2020 году:\n', *sel, '\n')

sel = connection.execute("""SELECT title_collection
FROM performers A
JOIN performers_albums B ON A.id = B.performers_id
JOIN albums C ON B.albums_id = C.id
JOIN tracks D ON C.id = D.albums_id
JOIN collection_track E ON D.id = E.tracks_id
JOIN collection F ON E.collection_id = F.id
WHERE name_performers = 'Madonna'
""")
print('названия сборников, в которых присутствует конкретный исполнитель (Madonna):\n', *sel, '\n')

sel = connection.execute("""SELECT title_albums
FROM albums A 
JOIN performers_albums B ON A.id = B.albums_id
JOIN performers C ON B.performers_id = C.id
JOIN performers_ganre D ON C.id = D.performers_id
JOIN genre E ON D.genre_id = E.id
GROUP BY A.title_albums
HAVING COUNT(DISTINCT E.title_genre) > 1
ORDER BY A.title_albums

""")
print('название альбомов, в которых присутствуют исполнители более 1 жанра:\n', *sel, '\n')

sel = connection.execute("""SELECT track_name
FROM tracks A
FULL OUTER JOIN collection_track B ON A.id = B.tracks_id
WHERE A.id IS NULL
OR B.tracks_id IS NULL
""")
print('наименование треков, которые не входят в сборники:\n', *sel, '\n')

sel = connection.execute("""SELECT name_performers, track_name, MIN(duration)
FROM performers A
JOIN performers_albums B ON A.id = B.performers_id
JOIN albums C ON B.albums_id = C.id
JOIN tracks D ON C.id = D.albums_id
WHERE D.duration = (
    SELECT MIN(duration) FROM tracks D )
GROUP BY A.name_performers, d.track_name;
""")
print('Исполнители написавшие самые короткие по продолжительности треки:\n', *sel, '\n')

sel = connection.execute("""SELECT A.title_albums, COUNT(B.ID)
FROM albums A
JOIN tracks B ON A.id = B.albums_id
WHERE B.albums_id in (
    SELECT albums_id
    FROM tracks
    GROUP BY albums_id
    HAVING COUNT(id) = (
        SELECT COUNT(id)
        FROM tracks
        GROUP BY albums_id
        ORDER BY COUNT
        LIMIT 1))   
GROUP BY A.title_albums
ORDER BY COUNT(B.ID)  DESC;      
""")
print('название альбомов, содержащих наименьшее количество треков:\n', *sel, '\n')