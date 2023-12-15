import requests
import json
import datetime
from service_specific_adapter_base import ServiceSpecificAdapterBase
import pandas as pd
from datetime import datetime, timedelta
import os


server = 'http://genericadapter:9090'

class ClientAdapter(ServiceSpecificAdapterBase):
    def __init__(self, server):
        super().__init__(server)


if __name__ == "__main__":
    ga = ClientAdapter(server)
    
    ga.service_store_login(os.getenv('ga_user'), os.getenv('ga_password')) 
    knowledge_base_name = 'SSAClient'
    knowledge_base_description = 'SSAClient'
    knowledge_base_id = 'https://ke.interconnectproject.eu/rest/adapter/RecommenderSSAClient'
    ga.knowledge_base_id = knowledge_base_id
    ga.add_knowledge_base(knowledge_base_id, knowledge_base_name, knowledge_base_description)

    graph_pattern = open('/home/ai4cs/interoperable_recommender_graph_pattern.gp').read()
    prefixes = {
        "dc":"http://purl.org/dc/elements/1.1/",
        "gn":"https://www.geonames.org/ontology#",
        "s4ener":"https://saref.etsi.org/saref4ener/",
        "ic-data":"http://ontology.tno.nl/interconnect/datapoint#",
        "time":"http://www.w3.org/2006/time#",
        "saref":"https://saref.etsi.org/corehasTime",
        "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "iso3166":"http://purl.org/dc/terms/ISO3166",
        "xsd":"http://www.w3.org/2001/XMLSchema#"
    }

    kiid = ga.add_knowledge_interaction(knowledge_base_description,knowledge_interaction_type='AskKnowledgeInteraction',knowledgeInteractionName = 'getRecommendations',graph_pattern = graph_pattern,prefixes = prefixes)


    tomorrow_date = datetime.now() + timedelta(days=1)
    formatted_start_date_time = tomorrow_date.strftime("<%Y-%m-%dT00:00>")
    formatted_end_date_time = tomorrow_date.strftime("<%Y-%m-%dT23:00>")

    input_bindings = []
    map = {}
    map["country_code"] = "<PT>"
    map["start_datetime"] = formatted_start_date_time
    map["end_datetime"] = formatted_end_date_time
    input_bindings.append(map)  

    print("sending ask request")
    output_bindingset = ga.ask_request(json.loads(kiid)['knowledgeInteractionId'],input_bindings)
    print(output_bindingset)
    if output_bindingset:
        df = pd.DataFrame.from_dict(output_bindingset)
        #print(output_bindingset)
        df=df.replace({'<':''}, regex=True)
        df=df.replace({'>':''}, regex=True)
        from sqlalchemy import create_engine
        engine = create_engine('postgresql://'+os.getenv("POSTGRES_USER")+':'+os.getenv("POSTGRES_PASSWORD")+'@'+os.getenv("POSTGRES_HOST")+':5432/'+os.getenv("POSTGRES_DB"))
        df.to_sql('energy_app_recommender', engine, if_exists='append', index=False)
    else:
        print ('Output is empty')

    ga.remove_knowledge_base(knowledge_base_id)
