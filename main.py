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
    return run_query("SELECT * FROM top_three")
    # db = psycopg2.connect(database=DBNAME)
    # cursor = db.cursor()
    # cursor.execute("SELECT * FROM top_three")
    # results = cursor.fetchall()
    # db.close()
    # return results


def top_authors():
    return run_query('select * from top_authors')


def top_errors():
    return run_query("""
        SELECT to_char(time::date, 'YYYY-MM-DD') AS day, round((sum(CASE WHEN status NOT LIKE '%200%' THEN 1 ELSE 0 END) / (count(*) * 1.0) * 100.0), 2) AS percent_errors
        FROM log
        GROUP BY day
        HAVING (sum(CASE WHEN status NOT LIKE '%200%' THEN 1 ELSE 0 END) / (count(*) * 1.0) * 100.0) >= 1.0
        ORDER BY percent_errors DESC;
        """)


def test_query(content):
    display_content = ""
    for row in content:
        display_content += "{0:<48} | {1:<48}\n".format(*row)
    return display_content


def display_rows(content, column_1_name, column_2_name):
    display_content = "{:_<98}\n".format(" ")
    display_content += "|{0:^48}|{1:^48}|\n".format(
        column_1_name, column_2_name)
    display_content += "|{:-^48}|{:-^48}|\n".format("", "")

    for row in content:
        display_content += "|{:^48}|{:^48}|\n".format("", "")
        display_content += "|{0:^48}|{1:^48}|\n".format(*row)

    display_content += "|{:_<48}|{:_<48}|\n".format("", "")

    return display_content


def main():
    print "Preparing for launch...\n"
    stories = top_three()
    print "Firing up the engines...\n"
    authors = top_authors()
    print "3, 2, 1..."
    errors = top_errors()
    print "{:^98}".format("Top Three")
    print display_rows(stories, "Articles", "Views")
    print "{:^98}".format("Top Authors")
    print display_rows(authors, "Author", "Views")
    print "{:^98}".format("Day with highest Error count")
    # print errors
    print display_rows(errors, "Day", "Errors")
    # errors = top_errors()
    # print test_query(errors)


main()
# test_query()
