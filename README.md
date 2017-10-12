# logs-analysis
Logs analysis project for Udacity

### Code Design

This code makes use of three custom functions.

  ```python
  run_query(), display_rows()
  ```
  and 
  ```
  main()
  ```

```python
run_query()
```

### Views

Run each of these three statements in the postgreSQL terminal

#### Top Three Articles
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
```sql
CREATE VIEW ranked_authors AS
    SELECT authors.name, count(authors.name) AS views
        FROM authors, articles, log
        WHERE log.path LIKE concat ('%', articles.slug) AND articles.author = authors.id
        GROUP BY authors.name
        ORDER BY views DESC;
```

#### Days with errors above 1%
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
