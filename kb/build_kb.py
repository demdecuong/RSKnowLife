'''
Author: Nguyen Phuc Minh
Lastest update: 18/3/2022
'''

import os
import pandas as pd
import logging
import json

from py2neo import Graph,Node
from typing import Text, List, Dict
from constants import *
from tqdm import tqdm

class KnowledgeGraph():
    def __init__(self,
                uri: Text = None,
                user: Text = None,
                password: Text = None,
                db_name: Text = 'vinbrain',
                disease_path: Text = DISEASE_PATH,
                symptom_path: Text = SYMPTOM_PATH,
                specialty_path: Text = SPECIALTY_PATH,
                disease_symptom_path: Text = DISEASE_SYMPTOM_PATH,
                disease_specialty_path: Text = DISEASE_SPECIALTY_PATH,
                doctor_path: Text = DOCTOR_PATH,
                patient_path: Text = PATIENT_PATH) -> None:
        
        # node
        self.disease = pd.read_csv(disease_path)
        self.symptom = pd.read_csv(symptom_path)
        self.specialty = pd.read_csv(specialty_path)
        self.doctor = pd.read_csv(doctor_path)
        self.patient = pd.read_csv(patient_path)
     
        # relationship
        self.disease_symptom_rel = pd.read_csv(disease_symptom_path)
        self.disease_specialty_rel = pd.read_csv(disease_specialty_path)
        
        self.graph = Graph(uri, auth=(user, password))

        self.disease = self.normalize_csv(self.disease)
        self.symptom = self.normalize_csv(self.symptom)
        self.specialty = self.normalize_csv(self.specialty)
        self.doctor = self.normalize_csv(self.doctor)
        self.patient = self.normalize_csv(self.patient)

        self.db_name = db_name

    def normalize_csv(self,data:pd.DataFrame)->pd.DataFrame:
        return data.fillna("No Info")
        
    def init_database(self) -> None:
        print(f"Init database {self.db_name}")
        cypher_ = f"CREATE DATABASE {self.db_name} IF NOT EXISTS"
        self.graph.run(cypher_)
        return

    def read_nodes(self) -> List[Dict]:
        DISEASE = []
        SYMPTOM = []
        SPECIALTY = []
        
        DISEASE_SYMPTOM = []
        DISEASE_SPECIALTY = []
        
        DOCTOR = []
        PATIENT = []

        # disease - node
        for index, row in self.disease.iterrows():
            DISEASE.append({
                "id":row['id'],
                "name":row['name'],
                "overview":row['overview'],
                "cause":row['cause'],
                "symptom":row['symptom'],
                "risk_factor":row['risk_factor'],
                "treatment":row['treatment'],
                "diagnosis":row['diagnosis'],
                "prevention":row['prevention'],
                "severity":row['severity'],
                "synonym":row['synonym']
            })
        
        # symptom - node
        for index, row in self.symptom.iterrows():
            SYMPTOM.append({
                "id":row['id'],
                "name":row['name'],
                "overview":row['overview'],
            })
            
        # specialty - node
        for index, row in self.specialty.iterrows():
            SPECIALTY.append({
                "id":row['id'],
                "name":row['name'],
                "description":row['description'],
            })
        
        # doctor - node
        for index, row in self.doctor.iterrows():
            DOCTOR.append({
                "id":row['id'],
                "name":row['name'],
                "gender":row['gender'],
                "age":row['age'],
                "title":row['title'],
                "speciality":row['speciality'],
                "review":row['review'],
                "hourly_rate":row['hourly_rate'],
                "experience":row['experience'],
            })

        # patient - node
        for index, row in self.patient.iterrows():
            PATIENT.append({
                "id":row['id'],
                "name":row['name'],
                "gender":row['gender'],
                "income":row['income'],
                "address":row['address'],
                "age":row['age'],
            })

        # disease-symptom rels
        for index, row in self.disease_symptom_rel.iterrows():
            DISEASE_SYMPTOM.append({
                "disease_id":row['disease_id'],
                "symptom_id":row['symptom_id']
            })
        
        # disease-specialty rels
        for index, row in self.disease_specialty_rel.iterrows():
            DISEASE_SPECIALTY.append({
                "disease_id":row['disease_id'],
                "specialty_id":row['specialty_id']
            })      
            
        return DISEASE, SYMPTOM, SPECIALTY, DOCTOR, PATIENT, DISEASE_SYMPTOM, DISEASE_SPECIALTY
    
    def remove_nodes(self) -> None:
        ''' Clear all database
        '''
        print("Remove all nodes,  relationships")
        cypher = 'MATCH (n) DETACH DELETE n'
        self.graph.run(cypher)
        
    def create_nodes(self) -> None:
        # self.init_database()
        self.remove_nodes()

        DISEASE, SYMPTOM, SPECIALTY, DOCTOR, PATIENT, DISEASE_SYMPTOM, DISEASE_SPECIALTY = self.read_nodes()
        
        # disease
        print("Create disease node")
        for node in tqdm(DISEASE):
            cypher_ = "CREATE (d:Disease $props) RETURN d"
            self.graph.run(cypher_,props=node)
        
        #symptom
        print("Create symptom node")
        for node in tqdm(SYMPTOM):
            cypher_ = "CREATE (d:Symptom $props) RETURN d"
            self.graph.run(cypher_,props=node)
        
        # specialty
        print("Create specialty node")
        for node in tqdm(SPECIALTY):
            cypher_ = "CREATE (d:Specialty $props) RETURN d"
            self.graph.run(cypher_,props=node)

        # doctor
        print("Create doctor node")
        for node in tqdm(DOCTOR):
            cypher_ = "CREATE (d:Doctor $props) RETURN d"
            self.graph.run(cypher_,props=node)
        
        # patient
        print("Create patient node")
        for node in tqdm(PATIENT):
            cypher_ = "CREATE (d:Patient $props) RETURN d"
            self.graph.run(cypher_,props=node)

        # disease-symptom rels
        print("Create disease-symptom relation")
        for rel in tqdm(DISEASE_SYMPTOM):
            disease_id = rel['disease_id']
            symptom_id = rel['symptom_id']
            cypher_ = f'''
            MATCH (d:Disease), (s:Symptom)
            WHERE d.id = {disease_id} AND s.id = {symptom_id}
            CREATE (d)-[r:HAS_SYMPTOM]->(s)
            RETURN type(r)
            '''
            self.graph.run(cypher_)

        # disease-specialty rels
        print("Create disease-specialty relation")
        for rel in tqdm(DISEASE_SPECIALTY):
            disease_id = rel['disease_id']
            symptom_id = rel['specialty_id']
            cypher_ = f'''
            MATCH (d:Disease), (s:Specialty)
            WHERE d.id = {disease_id} AND s.id = {symptom_id}
            CREATE (d)-[r:HAS_SPECIALTY]->(s)
            RETURN type(r)
            '''
            self.graph.run(cypher_)

        return

if __name__ == "__main__":
    NEO4J_URL = os.getenv("NEO4J_URL", None)
    NEO4J_AUTH = os.getenv("NEO4J_AUTH", None)
    user = NEO4J_AUTH.split("/")[0]
    password = NEO4J_AUTH.split("/")[1]
    
    kg = KnowledgeGraph(NEO4J_URL, user, password)

    kg.create_nodes()
