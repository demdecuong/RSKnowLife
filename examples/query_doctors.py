import os
from kb.neo4j_provider import Neo4jProvider

NEO4J_URL = os.getenv("NEO4J_URL", None)
NEO4J_AUTH = os.getenv("NEO4J_AUTH", None)
user = NEO4J_AUTH.split("/")[0]
password = NEO4J_AUTH.split("/")[1]
service = Neo4jProvider(NEO4J_URL, user, password)


request = {
    'symptom' : "chóng mặt",
    'speciality' : 'thần kinh',
    'disease':''
}

doctors = service.query_doctors(request)
print(doctors)
