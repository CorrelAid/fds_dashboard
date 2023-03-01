# QUERIES USED TO UPDATE / INSERT NEW DATA



# TEMPORARY TABLE CREATION

create_tmp_jurisdictions = """CREATE TABLE tmp_jurisdictions (LIKE jurisdictions INCLUDING ALL)"""

create_tmp_public_bodies = """CREATE TABLE tmp_public_bodies (LIKE public_bodies INCLUDING ALL)"""

create_tmp_foi_requests = """CREATE TABLE tmp_foi_requests (LIKE foi_requests INCLUDING ALL)"""

create_tmp_messages = """CREATE TABLE tmp_messages (LIKE messages INCLUDING ALL)"""

# UPSERT DATA into temp tables
# issue: statements are fixed regarding no of columns, need to be changed in case that format of updated data / tables change

upsert_tmp_jurisdictions = f"INSERT INTO tmp_jurisdictions VALUES (?,?,?) ON CONFLICT (id) DO UPDATE"

upsert_tmp_public_bodies = f"INSERT INTO tmp_public_bodies VALUES (?,?,?,?,?,?) ON CONFLICT (id) DO UPDATE"

upsert_tmp_foi_requests = f"INSERT INTO tmp_foi_requests VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT (id) DO UPDATE"

upsert_tmp_messages = f"INSERT INTO tmp_messages VALUES (?,?,?,?,?,?,?,?,?,?) ON CONFLICT (id) DO UPDATE"

# MERGE DATA from temp to target

merge_jurisdiction = """
MERGE jurisdictions AS Target USING tmp_jurisdictions AS Source ON Target.id=Source.id 
WHEN NOT MATCHED INSERT VALUES (Source.id, Source.name, Source.rank) 
WHEN MATCHED UPDATE SET Target.name=Source.name, Target.rank=Source.rank"""

merge_public_bodies = """
MERGE public_bodies AS Target USING tmp_public_bodies AS Source ON Target.id=Source.id 
WHEN NOT MATCHED INSERT VALUES (Source.id, Source.name, Source.classification, Source.categories, Source.address, Source.jurisdiction)
WHEN MATCHED UPDATE SET Target.name=Source.name, Target.classification=Source.classification, Target.categories=Source.categories, Target.address=Source.address, Target.jurisdiction=Source.jurisdiction
"""

merge_foi_requests = """
MERGE foi_requests AS Target USING tmp_foi_requests AS Source ON Target.id=Source.id
WHEN NOT MATCHED INSERT VALUES (Source.id, Source.jurisdiction, Source.refusal_reason, Source.costs, Source.due_date, Source.resolved_on, Source.first_message, Source.last_message, Source.status, Source.resolution, Source.user_id, Source.public_body_id)
WHEN MATCHED UPDATE SET Target.jurisdiction=Source.jurisdiction, 
                        Target.refusal_reason=Source.refusal,
                        Target.costs=Source.costs,
                        Target.due_date=Source.due_date,
                        Target.resolved_on=Source.resolved_on,
                        Target.first_message=Source.first_message,
                        Target.last_message=Source.last_message,
                        Target.status=Source.status,
                        Target.resolution=Source.resolution,
                        Target.user_id=Source.user_id,
                        Target.public_body_id=Source.public_body_id
"""

merge_messages = """
MERGE messages AS Target USING tmp_messages ON Target.id=Source.id
WHEN NOT MATCHED INSERT VALUES (Source.id, Source.request, Source.sent, Source.is_response, Source.is_postal, Source.kind, Source.sender_public_body, Source.recipient_public_body, Source.status, Source.timestamp)
WHEN MATCHED UPDATE SET Target.request=Source.request,
                        Target.sent=Source.sent,
                        Target.is_response=Source.is_response,
                        Target.is_postal=Source.is_postal,
                        Target.kind=Source.kind,
                        Target.sender_public_body=Source.sender_public_body,
                        Target.recipient_target_body=Source.recipient_target_body,
                        Target.status=Source.status,
                        Target.timestamp=Source.timestamp
"""



# TEMPORARY TABLE DELETION

delete_tmp_jurisdictions = """DROP TABLE IF EXISTS tmp_jurisdictions"""

delete_tmp_public_bodies = """DROP TABLE IF EXISTS tmp_public_bodies"""

delete_tmp_foi_requests = """DROP TABLE IF EXISTS tmp_foi_requests"""

delete_tmp_messages = """DROP TABLE IF EXISTS tmp_messages"""