# Healthcare Professional Recommendation System

### Installation

1. Packages
```bash
pip install -r requirements.txt
```

2. Neo4j

Go to `data/README.md` for the instructions.

### Data
Please place data into `kb/data/` directory.
There will be a script for download data later.

### Usage

1. Build KB
```
bash run_build_db.sh
```
This will takes a while. I will code the option for creating nodes only soon.

2. Query database
```bash
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

doctors = service.query_doctors(request) # List[Dict]
```