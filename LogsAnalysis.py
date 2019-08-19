#!/usr/bin/env python3
import psycopg2


# Conect to DB
def init_query(query):
    try:
        db = psycopg2.connect("dbname=news")
        c = db.cursor()
        c.execute(query)
        query = c.fetchall()
        db.close()
        return query
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)


# Query to question 1
def question_1():
    # Relate the articles slug with log's path and count to get
    # the most popular article orderin by desc and output 3
    print("1-What are the most popular three articles of all time?\n")
    result = init_query("""
    SELECT articles.title, count(*) as num
    FROM articles, log where articles.slug = substr(log.path,10)
    AND log.status = '200 OK'
    GROUP BY articles.title
    ORDER BY num DESC limit 3;""")
    for r in result:
        x = str(r[0]) + ': ' + str(r[1]) + ' views'
        print(x)
    print("\n")


# Query to question 2
def question_2():
    # Relate slug from article with path from log, and id from
    # authors with author from articles to count the succesfull logs by author
    # and order them by desc
    print("2-Who are the most popular article authors of all time?\n")
    result = init_query("""
    SELECT authors.name, count(*) as num
    FROM articles, log, authors
    WHERE articles.slug = substr(log.path,10) AND log.status = '200 OK'
    AND articles.author = authors.id
    GROUP BY authors.name
    ORDER BY num DESC limit 4;""")
    for r in result:
        x = str(r[0]) + ': ' + str(r[1]) + ' views'
        print(x)
    print("\n")


# Query to question 3
def question_3():
    print("""3-On which days did more than 1% of requests lead to errors?""")
    # Create a new table from log to get the days user log
    # in and the total ok logs
    # Then an other table to get the erros  by day
    # Join them to get the day with more than 1% of erros
    result = init_query("""
    SELECT total_date.date, (1.0*total_error.errors)/total_date.num as porc
    FROM (
        SELECT
        date_trunc('day', time) date,
        COUNT (*) as num
        FROM log
        GROUP BY date
    ) AS total_date
    JOIN (
        SELECT
        date_trunc('day', time) errors_date, COUNT (*) as errors
        FROM log WHERE status = '404 NOT FOUND' GROUP BY errors_date
    ) AS total_error
    ON total_date.date = total_error.errors_date
    WHERE (total_error.errors*100/total_date.num)> 1
    ORDER BY porc
    ;
    """)

    for r in result:
        date = str(r[0].strftime('%B %d , %Y'))
        porc = str(round(r[1], 3) * 100)
        x = date + ' : ' + porc + '%'
        print(x)
    print("\n")


question_1()
question_2()
question_3()
