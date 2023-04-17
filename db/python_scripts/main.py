from rich.console import Console
from rich.status import Status
from helpers import dload

console = Console()

cols_foi_requests = ["id", "jurisdiction", "refusal_reason", "costs", "due_date", "resolved_on", "created_at", "last_message", "status", "resolution", "user", "public_body", "campaign","messages"]
cols_messages = ["id", "request", "sent", "is_response", "is_postal", "kind", "sender_public_body", "recipient_public_body", "status", "timestamp"]
cols_pbodies = ["id", "name", "classification", "categories", "address", "jurisdiction", ]
cols_campaigns=["id", "name", "slug", "url", "description", "start_date", "active"]

console.print("Hello :smiley:")
console.print("This script will download all FOI requests, messages, public bodies, jurisdictions and classification in the FDS database. It will only save specified columns.")
console.log("Starting Script.")
console.rule("")
console.log("Beginning to download FOI requests.")
dload("https://fragdenstaat.de/api/v1/request/", "foi_requests", "last_message", cols_foi_requests, console)
console.log("Done downloading FOI requests!")
console.rule("")
# console.log("Beginning to download messages")
# dload("https://fragdenstaat.de/api/v1/message/", "messages", "timestamp", cols_messages, console)
# console.log("Done downloading messages.")
console.rule("")
# console.log("Beginning to download public bodies.")
# dload("https://fragdenstaat.de/api/v1/publicbody/", "public_bodies", "id", cols_pbodies, console)
# console.log("Done downloading public bodies.")
dload("https://fragdenstaat.de/api/v1/campaign/", "campaigns", "start_date", cols_campaigns, console)
console.rule("")
console.log("Downloaded everything!")
console.print("Bye bye :smiley:")