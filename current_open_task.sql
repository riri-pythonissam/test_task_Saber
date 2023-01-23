
SELECT 
	issue_key,
	status,
	DATETIME(started_at/1000.0, 'unixepoch') as date_start 
FROM 
	history
WHERE 
	status != 'Closed' 
AND 
	status != 'Resolved'
AND 
	DATETIME('now') BETWEEN DATETIME(started_at/1000.0, 'unixepoch') AND DATETIME(ended_at/1000.0, 'unixepoch')
