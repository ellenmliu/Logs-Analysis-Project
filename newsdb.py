import psycopg2

d = psycopg2.connect(database="news")
cursor = d.cursor()

# What are the most popular three articles of all time?
query01 = "create view articleslogauthors as select author, title, slug,\
           path, status, to_char(log.time, 'FMMonth FMDDth, YYYY') as logdate,\
           name from articles, log, authors\
           where articles.slug =\
           (regexp_split_to_array(path, E'/article/'))[2] and\
           articles.author = authors.id"
query1 = "select title, count(*) as views from articleslogauthors\
          where (regexp_split_to_array(path, E'/article/'))[2] != '/'\
          group by title order by views desc limit 3;"
cursor.execute(query01)
cursor.execute(query1)
top_three_articles = cursor.fetchall()
print "Three Most Popular Articles of All Time\n"
for row in top_three_articles:
    print '"' + row[0] + '"' + '\t' + str(row[1]) + " views"

# Who are the most popular article authors of all time?
query2 = "select name, count(*) as views\
          from articleslogauthors where status != '404 NOT FOUND'\
          group by name\
          order by views desc;"
cursor.execute(query2)
top_three_authors = cursor.fetchall()
print "\nThree Most Popular Article Authors of All Time\n"
for row in top_three_authors:
    print row[0] + '\t\t\t' + str(row[1]) + " views"

# On which days did more than 1% of requests lead to errors?
query03 = "create view errorsperday as select\
           to_char(log.time, 'FMMonth FMDDth, YYYY') as logdate,\
           count(log.time) as errors from log\
           where log.status = '404 NOT FOUND'\
           group by logdate"
query04 = "create view totalperday as select\
           to_char(log.time, 'FMMonth FMDDth, YYYY') as logdate,\
           count(log.time) as totalvisits from log\
           group by logdate"
query3 = "select errorsperday.logdate, errors, totalvisits,\
          round(round(errors,2) / round(totalvisits, 2)* 100,2) as percentage\
          from totalperday, errorsperday\
          where errorsperday.logdate = totalperday.logdate and\
          round(round(errors,2) / round(totalvisits, 2)* 100,2) > 1\
          order by percentage desc"
query4 = "select * from totalperday"
cursor.execute(query03)
cursor.execute(query04)
cursor.execute(query3)
error_percentage = cursor.fetchall()
print "\nDays Where More Than 1% of Requests Lead to Errors\n"
for row in error_percentage:
    print row[0] + '\t\t\t' + str(row[3]) + '% errors'

d.close()
