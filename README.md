# Logs Analysis Project

Author: Ellen Liu
Last Edit: 6/13/2017

Used PostgreSQL to report 3 questions:
    1) What are the most popular three articles of all time?
    2) Who are the most popular article authos of all time?
    3) On which days did more than 1% of requests lead to errors?

## `create views`
I used a few `create views` function. The first is called articleslofauthors,
which combined all three database into one. The article's author is the same as
author's id and part of the log's path is the same as the article's slug. That way
I can use this to answer the first questions.

The second and third view is used for the last question. I made one called errorsperday,
which had the count and date of the logs that had a status of '404 NOT FOUND' within each day
and the other is called totalperday, which had the count and date of all the logs within each day.
I used this so I can calculate the percentage and display which date(s) had more than 1% of
requests lead to errors.

## Requirements
You need the virtual machine, python and Vagrant installed onto your computer. Once it's installed
you would connect to the database and load the data from the `newsdata.sql`. Once the data is
loaded you may be able to move on to the next step.

Once everything is ready, you need to run the next three to make the three views in the psql command.

`create view articleslogauthors as select author, title, slug, path, status, to_char(log.time, 'FMMonth FMDDth, YYYY') as logdate,name from articles, log, authors where articles.slug = (regexp_split_to_array(path, E'/article/'))[2] and articles.author = authors.id;`

`create view errorsperday as select to_char(log.time, 'FMMonth FMDDth, YYYY') as logdate, count(log.time) as errors from log where log.status = '404 NOT FOUND' group by logdate;`

`create view totalperday as select to_char(log.time, 'FMMonth FMDDth, YYYY') as logdate, count(log.time) as totalvisits from log group by logdate;`


## To use
Download the zip file and unzip the file. Then open up terminal and `cd` to the vagrant folder.
Bring the virtual machine online and log in. Then `cd` to the database folder where `newsdb.py`
is stored and run the command `python newsdb.py`. It should show up with the three reports.
