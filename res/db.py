import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('students_bd.db') #установили связь с БД (или создали если ее нет)
        self.c = self.conn.cursor() #создали курсор
        #таблица Список групп
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "book" (
                       "id_book" INTEGER NOT NULL,
                       "invenatrni_nomer" INTEGER,
                       "name_book" INTEGER,
                       "god_izdaniya" INTEGER,
                       "kolvo_stranic" INTEGER,
                       "price" INTEGER,
                       "id_izdatelstvo" INTEGER,
                       "id_mesto_izdaniya" INTEGER,
                       "id_author" INTEGER,
                       "id_vidacha" INTEGER,
                       "id_vozvrat" INTEGER,
                       "id_ganre" INTEGER,
                       PRIMARY KEY("id_book" AUTOINCREMENT)
                        )'''
            )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "author" (
                        "id_author" INTEGER NOT NULL,
                        "name" TEXT,
                        "familiya" TEXT,
                        "otchestvo" TEXT,
                        PRIMARY KEY("id_author" AUTOINCREMENT)
                        )'''
        )
        #таблица Специальности
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "place_publication" (
                        "id_place" INTEGER,
                        "name_place" TEXT,
                        PRIMARY KEY("id_place" AUTOINCREMENT)
                        )'''
            )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "publish_house" (
                        "id_publish" INTEGER NOT NULL,
                        "name_publish" TEXT,
                        PRIMARY KEY("id_publish" AUTOINCREMENT)
                        )'''
            )
        #таблица Студенты
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "student" (
                        "id_student" INTEGER NOT NULL,
                        "name" TEXT,
                        "surname" TEXT,
                        "patronymic" TEXT,
                        PRIMARY KEY("id_student" AUTOINCREMENT)
                        )'''
            )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "spis" (
                        "id_wrofbook" INTEGER NOT NULL,
                        "name_book" TEXT,
                        "prich_spis" TEXT,
                        PRIMARY KEY("id_wrofbook" AUTOINCREMENT)
                        )'''
            )
        #таблица Отделение
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "extradition" (
                        "id_extradition" INTEGER NOT NULL,
                        "date" TEXT,
                        "id_student" INTEGER,
                        "book" TEXT,
                        PRIMARY KEY("id_extradition" AUTOINCREMENT)
                        )'''
            )
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "refund" (
                        "id_refund" INTEGER NOT NULL,
                        "date" TEXT,
                        "id_student" INTEGER,
                        "book" TEXT,
                        PRIMARY KEY("id_refund" AUTOINCREMENT)
                        )'''
            )
        self.c.execute (
            '''CREATE TABLE IF NOT EXISTS "genre" (
                        "id_genre" INTEGER NOT NULL,
                        "name_genre" TEXT,
                        PRIMARY KEY ("id_genre" AUTOINCREMENT)
                        )'''
            )
        
        self.conn.commit()

db = DB()
