'''
Author: Nguyen Phuc Minh
Lastest update: 18/3/2022
'''

import os
import itertools

from typing import Text, List, Dict
from py2neo import Graph, Node

class Neo4jProvider():
    def __init__(self, uri: Text = None, user: Text = None, password: Text = None):
        if not uri:
            uri = NEO4J_URL
            user = NEO4J_AUTH.split("/")[0]
            password = NEO4J_AUTH.split("/")[1]
        self.graph = Graph(uri, auth=(user, password))

    def query_doctors(self,request:Dict) -> List[Dict]:
        ''' Query doctor from database
        Args:
            - request : {
                'symptom' (str)
                'speciality' (str)
                'disease' (str)
            }
        Return:
        '''
        # get relevant doctors by specility
        try:
            doctors = self.get_doctors_by_speciality(request['speciality'])
            return doctors
        except:
            print(f"No doctor has speciality is {request['speciality']}")
            return [{}]

    def get_doctors_by_speciality(self,speciality:Text) -> List[Dict]:
        query = f"""
            MATCH (s:Doctor)
            WHERE s.speciality = "thần kinh"
            RETURN s
            """

        ans = self.graph.run(query).data()
        return ans


