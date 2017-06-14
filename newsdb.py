#! /usr/bin/env python3
import psycopg2


# What are the most popular three articles of all time?
def most_pop_articles():
    d = psycopg2.connect(database="news")
    cursor = d.cursor()
    query1 = "select title, count(*) as views from articleslogauthors\
              where (regexp_split_to_array(path, E'/article/'))[2] != '/'\
              group by title order by views desc limit 3;"
    cursor.execute(query1)
    top_three_articles = cursor.fetchall()
    print "Three Most Popular Articles of All Time\n"
    for row in top_three_articles:
        print "{:<25s}{:>25s}".format('"' + row[0] + '"', str(row[1]) +
                                      " views")
    d.close()


# Who are the most popular article authors of all time?
def most_pop_authors():
    d = psycopg2.connect(database="news")
    cursor = d.cursor()
    query2 = "select name, count(*) as views\
              from articleslogauthors where status != '404 NOT FOUND'\
              group by name\
              order by views desc;"
    cursor.execute(query2)
    top_three_authors = cursor.fetchall()
    print "\nThree Most Popular Article Authors of All Time\n"
    for row in top_three_authors:
        print "{:<25s}{:>25s}".format(row[0], str(row[1]) + " views")
    d.close()


# On which days did more than 1% of requests lead to errors?
def error_percentage():
    d = psycopg2.connect(database="news")
    cursor = d.cursor()
    query3 = "select errorsperday.logdate, errors, totalvisits,\
              round(round(errors,2) / round(totalvisits, 2)* 100,2) as\
              percentage from totalperday, errorsperday\
              where errorsperday.logdate = totalperday.logdate and\
              round(round(errors,2) / round(totalvisits, 2)* 100,2) > 1\
              order by percentage desc"
    query4 = "select * from totalperday"
    cursor.execute(query3)
    error_percentage = cursor.fetchall()
    print "\nDays Where More Than 1% of Requests Lead to Errors\n"
    for row in error_percentage:
        print "{:<25s}{:>25s}".format(row[0], str(row[3]) + '% errors')
    d.close()

most_pop_articles()
most_pop_authors()
error_percentage()
