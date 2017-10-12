# logs-analysis
Logs analysis project for Udacity

### Code Design

This code makes use of three custom functions.

```python
run_query()
```
This function takes in a string which must be a proper SQL SELECT statement and returns a result set from the database.

```python
display_rows()
```
This function is a somewhat generic function for taking the results of `run_query()` and formatting for display. Returns
formatted results as a string.

```python
main()
```
The `main()` function is the primary function called to run the program. It initializes the different database queries and
then wraps them in some formatting for human readability.

### Views

Run each of these three statements in the postgreSQL terminal in order for programm to function correctly. Alternatively you could alter the `run_query()` calls and insert the portion starting with `SELECT` as the `query` argument.

#### Top Three Articles
Creates VIEW to retrieve the top three most popular articles.
```sql
CREATE VIEW top_three AS
    SELECT articles.title, count(articles.slug) AS views
        FROM articles, log
        WHERE log.path LIKE concat ('%', articles.slug)
        GROUP BY articles.title
        ORDER BY views DESC
        LIMIT 3;
```

#### Authors Ranked by Views
Creates VIEW to rank the authors based of number of views of all articles.
```sql
CREATE VIEW ranked_authors AS
    SELECT authors.name, count(authors.name) AS views
        FROM authors, articles, log
        WHERE log.path LIKE concat ('%', articles.slug) AND articles.author = authors.id
        GROUP BY authors.name
        ORDER BY views DESC;
```

#### Days with errors above 1%
Creates VIEW to find percentage of errors over 1% for any day.
```sql
CREATE VIEW high_errors AS
    SELECT to_char(time::date, 'YYYY-MM-DD') AS day,
            round((sum(CASE WHEN status NOT LIKE '%200%' THEN 1 ELSE 0 END) / (count(*) * 1.0) * 100.0), 2)
            AS percent_errors
        FROM log
        GROUP BY day
        HAVING (sum(CASE WHEN status NOT LIKE '%200%' THEN 1 ELSE 0 END) / (count(*) * 1.0) * 100.0) >= 1.0
        ORDER BY percent_errors DESC;
```

### How to run

navigate to `/vagrant/logs-analysis/` and run:
```bash
python main.py
```
or
```bash
./main.py
```
