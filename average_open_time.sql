SELECT SUBSTRING(issue_key, 1, 1) as gr, SUM(minutes_in_status)/COUNT(minutes_in_status) as average_open_time  FROM history
WHERE status = 'Open'
GROUP BY SUBSTRING(issue_key, 1, 1)
ORDER BY 2 ASC 