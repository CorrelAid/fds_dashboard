# QUERIES USED TO UPDATE / INSERT NEW DATA



# TEMPORARY TABLE CREATION

create_tmp_jurisdictions = """CREATE TABLE tmp_jurisdictions (LIKE jurisdictions INCLUDING ALL)"""

create_tmp_public_bodies = """CREATE TABLE tmp_public_bodies (LIKE public_bodies INCLUDING ALL)"""

create_tmp_foi_requests = """CREATE TABLE tmp_foi_requests (LIKE foi_requests INCLUDING ALL)"""

create_tmp_messages = """CREATE TABLE tmp_messages (LIKE messages INCLUDING ALL)"""



# MERGE DATA from temp to target

merge_jurisdiction = """
MERGE INTO jurisdictions AS Target USING tmp_jurisdictions AS Source ON Target.id=Source.id 
WHEN NOT MATCHED THEN INSERT (id, name, rank) VALUES (Source.id, Source.name, Source.rank) 
WHEN MATCHED THEN UPDATE SET name = Source.name, rank = Source.rank"""

merge_public_bodies = """
MERGE INTO public_bodies AS Target USING tmp_public_bodies AS Source ON Target.id=Source.id 
WHEN NOT MATCHED THEN INSERT VALUES (Source.id, Source.name, Source.classification, Source.categories, Source.address, Source.jurisdiction)
WHEN MATCHED THEN UPDATE SET name=Source.name, classification=Source.classification, categories=Source.categories, address=Source.address, jurisdiction=Source.jurisdiction
"""

merge_foi_requests = """
MERGE INTO foi_requests AS Target USING tmp_foi_requests AS Source ON Target.id=Source.id
WHEN NOT MATCHED THEN INSERT VALUES (Source.id, Source.jurisdiction, Source.refusal_reason, Source.costs, Source.due_date, Source.resolved_on, Source.first_message, Source.last_message, Source.status, Source.resolution, Source.user_id, Source.public_body_id)
WHEN MATCHED THEN UPDATE SET jurisdiction=Source.jurisdiction, 
                        refusal_reason=Source.refusal,
                        costs=Source.costs,
                        due_date=Source.due_date,
                        resolved_on=Source.resolved_on,
                        created_at=Source.first_message,
                        last_message=Source.last_message,
                        status=Source.status,
                        resolution=Source.resolution,
                        user_id=Source.user_id,
                        public_body_id=Source.public_body_id
"""

merge_messages = """
MERGE INTO messages AS Target USING tmp_messages ON Target.id=Source.id
WHEN NOT MATCHED THEN INSERT VALUES (Source.id, Source.request, Source.sent, Source.is_response, Source.is_postal, Source.kind, Source.sender_public_body, Source.recipient_public_body, Source.status, Source.timestamp)
WHEN MATCHED THEN UPDATE SET request=Source.request,
                        sent=Source.sent,
                        is_response=Source.is_response,
                        is_postal=Source.is_postal,
                        kind=Source.kind,
                        sender_public_body=Source.sender_public_body,
                        recipient_target_body=Source.recipient_target_body,
                        status=Source.status,
                        timestamp=Source.timestamp
"""



# TEMPORARY TABLE DELETION

delete_tmp_jurisdictions = """DROP TABLE IF EXISTS tmp_jurisdictions"""

delete_tmp_public_bodies = """DROP TABLE IF EXISTS tmp_public_bodies"""

delete_tmp_foi_requests = """DROP TABLE IF EXISTS tmp_foi_requests"""

delete_tmp_messages = """DROP TABLE IF EXISTS tmp_messages"""