#!/usr/bin/env python
# Author: Kevin Wing
# Created: 10/8/2017
# Modified: 10/8/2017

"""Execute these statements in postgreSQL for code to work properly.

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
        WHERE log.path LIKE concat ('%', articles.slug)
            AND articles.author = authors.id
        GROUP BY authors.name
        ORDER BY views DESC;

CREATE VIEW high_errors AS
    SELECT to_char(time::date, 'YYYY-MM-DD') AS day,
            round((sum(CASE WHEN status NOT LIKE '%200%' THEN 1 ELSE 0 END) /
                (count(*) * 1.0) * 100.0), 2)
            AS percent_errors
        FROM log
        GROUP BY day
        HAVING (sum(CASE WHEN status NOT LIKE '%200%' THEN 1 ELSE 0 END) /
            (count(*) * 1.0) * 100.0) >= 1.0
        ORDER BY percent_errors DESC;
"""

import psycopg2

DBNAME = 'news'  # Set name of postgreSQL database to connect to


def run_query(query, db_name=DBNAME):
    """Return the results of a SQL SELECT query.

    keyword args:
    query string -- Any SQL statement starting with SELECT (required)
    db_name string -- Specify the name of the postgreSQL database to
    be used (default=DBNAME)
    """
    db = psycopg2.connect(database=db_name)
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def display_rows(content, message, is_ratio=True):
    """Return content formatted for display to terminal.

    keyword args:
    content list -- A list of tuples obtained from a SQL query
    message string -- A string used as the title of the formatted output
    is_ratio boolean -- A boolean used to determine if '%' or 'Views'
    should be added to end of line
    """
    display_content = message + ":\n\n"

    for row in content:
        if is_ratio:
            display_content += (" " * 4) + "{0} - {1}%\n".format(*row)
        else:
            display_content += (" " * 4) + "{0} - {1} Views\n".format(*row)

    return display_content


def main():
    """Execute queries and displays results to terminal."""
    print(chr(27) + "[2J")
    print("Gathering Data...")
    stories = run_query("SELECT * FROM top_three")
    authors = run_query("SELECT * FROM ranked_authors")
    errors = run_query("SELECT * FROM high_errors")
    print(chr(27) + "[2J")
    print(display_rows(stories, "Top Three Articles by Views", False))
    print(display_rows(authors, "Authors ranked by Views", False))
    print(display_rows(errors, "Days with errors above 1%"))


main()
