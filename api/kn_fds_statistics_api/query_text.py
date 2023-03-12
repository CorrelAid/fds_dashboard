sql_total_users = '''
SELECT COUNT(DISTINCT user_id)
FROM foi_requests;
'''

sql_jurisdictions = '''
SELECT id, name
FROM jurisdictions;
'''

sql_public_bodies = '''
SELECT id, name
FROM public_bodies;
'''

sql_ranking_pb = '''
WITH total_num as (SELECT public_body_id, COUNT(DISTINCT id)
		   	       FROM foi_requests
		           WHERE public_body_id is not null
   		   		   GROUP BY public_body_id),
resolved as (SELECT r.public_body_id, COUNT(DISTINCT r.id)
	     	 FROM foi_requests as r
	    	 WHERE r.id in (SELECT DISTINCT m.request
			    			FROM public.messages m
			    			WHERE m.status='resolved')
			 GROUP BY r.public_body_id),
res_date as (SELECT DISTINCT m.request, MIN(m.timestamp)
			 FROM messages m
			 WHERE status='resolved'
			 GROUP BY m.request),
unres as (SELECT DISTINCT m.request, MAX(timestamp)
		  FROM messages m
		  WHERE m.request NOT IN (SELECT DISTINCT request
								  FROM messages
								  WHERE status='resolved')
		  GROUP BY m.request),
late_res as (SELECT r.id
			 FROM foi_requests r JOIN res_date d ON r.id=d.request
			 AND r.due_date<d.min),
late_unres as (SELECT r.id
			   FROM foi_requests r JOIN unres u ON r.id=u.request
			   AND r.due_date<u.max),
late_all as (SELECT COALESCE(lr.id, lu.id) as id
		 FROM late_res lr FULL JOIN late_unres lu ON lr.id=lu.id),
late as (SELECT pb.id, COUNT(DISTINCT l.id)
		 FROM public_bodies pb JOIN foi_requests r ON pb.id=r.public_body_id
		 JOIN late_all l ON r.id=l.id
		 GROUP BY pb.id)
						
SELECT pb.name, tn.count as Anzahl,
(CAST(res.count as decimal(16,2))/tn.count) * 100 as Erfolgsquote,
l.count as Fristüberschreitungen, (CAST(l.count as decimal(16,2))/tn.count) * 100 as Verspätungsquote
FROM public.public_bodies pb JOIN resolved res ON pb.id=res.public_body_id
JOIN total_num tn ON pb.id=res.public_body_id
JOIN late l ON l.id=pb.id
WHERE pb.id=tn.public_body_id AND tn.public_body_id=res.public_body_id AND tn.count>50
ORDER BY Verspätungsquote ASC
LIMIT 10
'''

sql_ranking_jurisdictions='''
WITH total_num as (SELECT public_body_id, COUNT(DISTINCT id)
		   	       FROM foi_requests
		           WHERE public_body_id is not null
   		   		   GROUP BY public_body_id),
resolved as (SELECT r.public_body_id, COUNT(DISTINCT r.id)
	     	 FROM foi_requests as r
	    	 WHERE r.id in (SELECT DISTINCT m.request
			    			FROM public.messages m
			    			WHERE m.status='resolved')
			 GROUP BY r.public_body_id),
res_date as (SELECT DISTINCT m.request, MIN(m.timestamp)
			 FROM messages m
			 WHERE status='resolved'
			 GROUP BY m.request),
unres as (SELECT DISTINCT m.request, MAX(timestamp)
		  FROM messages m
		  WHERE m.request NOT IN (SELECT DISTINCT request
								  FROM messages
								  WHERE status='resolved')
		  GROUP BY m.request),
late_res as (SELECT r.id
			 FROM foi_requests r JOIN res_date d ON r.id=d.request
			 AND r.due_date<d.min),
late_unres as (SELECT r.id
			   FROM foi_requests r JOIN unres u ON r.id=u.request
			   AND r.due_date<u.max),
late_all as (SELECT COALESCE(lr.id, lu.id) as id
		 FROM late_res lr FULL JOIN late_unres lu ON lr.id=lu.id),
late as (SELECT pb.id, COUNT(DISTINCT l.id)
		 FROM public_bodies pb JOIN foi_requests r ON pb.id=r.public_body_id
		 JOIN late_all l ON r.id=l.id
		 GROUP BY pb.id)
						
SELECT j.name, SUM(tn.count) as Anzahl,
(CAST(SUM(res.count) as decimal(16,2))/SUM(tn.count)) * 100 as Erfolgsquote,
SUM(l.count) as Fristüberschreitungen,
(CAST(SUM(l.count) as decimal(16,2))/SUM(tn.count)) * 100 as Verspätungsquote
FROM public.public_bodies pb JOIN resolved res ON pb.id=res.public_body_id
JOIN total_num tn ON pb.id=res.public_body_id
JOIN late l ON l.id=pb.id JOIN jurisdictions j ON j.id=pb.jurisdiction
WHERE pb.id=tn.public_body_id AND tn.public_body_id=res.public_body_id AND tn.count>50
GROUP BY j.name
ORDER BY Fristüberschreitungen ASC
LIMIT 10
'''

# https://mode.com/blog/how-to-make-box-and-whisker-plot-sql/

