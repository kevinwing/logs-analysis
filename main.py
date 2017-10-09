#!/usr/bin/env python
# Author: Kevin Wing
# Created: 10/8/2017
# Modified: 10/8/2017

"""
CREATE VIEW top_three AS
    SELECT articles.title, count(articles.slug) AS views
        FROM articles, log
        WHERE log.path LIKE concat ('%', articles.slug)
        GROUP BY articles.title
        ORDER BY views DESC
        LIMIT 3;

CREATE VIEW top_authors AS
    SELECT authors.name, count(authors.name) AS views
        FROM authors, articles, log
        WHERE log.path LIKE concat ('%', articles.slug) AND articles.author = authors.id
        GROUP BY authors.name
        ORDER BY views DESC;
"""

import psycopg2

DBNAME = 'news'


def run_query(query, db_name=DBNAME):
    db = psycopg2.connect(database=db_name)
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def top_three():
    return run_query('select * from top_three')
    # db = psycopg2.connect(database=DBNAME)
    # cursor = db.cursor()
    # cursor.execute("SELECT * FROM top_three")
    # results = cursor.fetchall()
    # db.close()
    # return results


def top_authors():
    return run_query('select * from top_authors')


def top_errors():
    return run_query("SELECT time, status FROM log WHERE status NOT LIKE '%200%' ORDER BY ")


def display_rows(content, column_1, column_2):
    display_content = "{:_<98}\n".format(" ")
    display_content += "|{0:^48}|{1:^48}|\n".format(column_1, column_2)
    display_content += "|{:-^48}|{:-^48}|\n".format("", "")

    for row in content:
        display_content += "|{0:^48}|{1:^48}|\n".format(*row)

    display_content += "|{:_<48}|{:_<48}|\n".format("", "")

    return display_content


def main():
    # print "Preparing for launch...\n"
    # stories = top_three()
    # print "Firing up the engines...\n"
    # authors = top_authors()
    # print "3, 2, 1..."
    errors = top_errors()
    # print "{:^98}".format("Top Three")
    # print display_rows(stories, "Articles", "Views")
    # print "{:^98}".format("Top Authors")
    # print display_rows(authors, "Author", "Views")
    print "{:^98}".format("Day with highest Error count")
    # print errors
    print display_rows(errors, "Day", "Errors")


main()
