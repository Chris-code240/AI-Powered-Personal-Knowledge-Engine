import requests
import dotenv
import os
dotenv.load_dotenv()
api_url = os.getenv("API_HOST")

def query(q:str):
    try:
        response =  requests.post(url=api_url+"/query", json={"query":q})
        if response.ok:
            return response.json()
        raise Exception(str(response.reason))
    except Exception as e:
        return {"success":False, "message":str(e)}

def add_data(data:dict):
    try:
        for key,value in data:
            if key not in {"type","data_path", "metadata_"}:
                raise KeyError(f"Invalid Key '{key}'")
        if not isinstance(data['metadata_'], dict): raise AttributeError(f"Metadata_ must be of type 'dict'")

        response = requests.post(url = api_url + "data", json=data)
        if response.ok:
            return response.json()
        raise Exception(str(response.reason))
    except Exception as e:
        return {"success":False, "message":str(e)}