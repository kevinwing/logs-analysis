# logs-analysis
Logs analysis project for Udacity

### Views

```
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
```
