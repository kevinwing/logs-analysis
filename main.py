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

CREATE VIEW ranked_authors AS
    SELECT authors.name, count(authors.name) AS views
        FROM authors, articles, log
        WHERE log.path LIKE concat ('%', articles.slug) AND articles.author = authors.id
        GROUP BY authors.name
        ORDER BY views DESC;

CREATE VIEW high_errors AS
    SELECT to_char(time::date, 'YYYY-MM-DD') AS day, round((sum(CASE WHEN status NOT LIKE '%200%' THEN 1 ELSE 0 END) / (count(*) * 1.0) * 100.0), 2) AS percent_errors
        FROM log
        GROUP BY day
        HAVING (sum(CASE WHEN status NOT LIKE '%200%' THEN 1 ELSE 0 END) / (count(*) * 1.0) * 100.0) >= 1.0
        ORDER BY percent_errors DESC;
"""

import psycopg2
# from datetime import datetime

DBNAME = 'news'


def run_query(query, db_name=DBNAME):
    db = psycopg2.connect(database=db_name)
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def top_three_articles():
    return run_query("SELECT * FROM top_three")


def ranked_authors():
    return run_query("SELECT * FROM ranked_authors")


def errors_by_day():
    return run_query("SELECT * FROM high_errors")


def display_rows(content, message, is_ratio=True):
    display_content = message + ":\n\n"

    for row in content:
        if is_ratio:
            display_content += (" " * 4) + "{0} - {1}%\n".format(*row)
        else:
            display_content += (" " * 4) + "{0} - {1} Views\n".format(*row)

    return display_content


def main():
    print(chr(27) + "[2J")
    print("Gathering Data...")
    stories = top_three_articles()
    authors = ranked_authors()
    errors = errors_by_day()
    print(chr(27) + "[2J")
    print(display_rows(stories, "Top Three Articles by Views", False))
    print(display_rows(authors, "Authors ranked by Views", False))
    print(display_rows(errors, "Days with errors above 1%"))


main()
# test_query()
