import logging
import json
from Bio import Entrez
import os

# Set up logging
logging.basicConfig(filename='fetch_PubMed.log', level=logging.ERROR)

# Set up email
EMAIL = 'abc@gmail.com'

# Define your diseases dictionary here 
diseases_dict = dict()

def search_pubmed(query, max_results=10):
    try:
        Entrez.email = EMAIL  # Always provide your email
        query_with_filter = query + " AND free full text[sb]"  # Adding the free full text filter
        handle = Entrez.esearch(db='pubmed', 
                                sort='relevance', 
                                retmax=max_results,
                                retmode='xml', 
                                term=query_with_filter)
        results = Entrez.read(handle)

        if results['IdList'] == []:
            handle = Entrez.esearch(db='pubmed', 
                                sort='relevance', 
                                retmax=max_results,
                                retmode='xml', 
                                term=query)
            
            results = Entrez.read(handle)
        return results['IdList']
    except Exception as e:
        logging.error(f"Error occurred while searching PubMed: {e}")
        return []

def fetch_pubmed_details(id_list):
    try:
        Entrez.email = EMAIL 
        if len(id_list) == 0:
            return None
        ids = ','.join(id_list)
        handle = Entrez.efetch(db='pubmed', id=ids, retmode='xml')
        papers = Entrez.read(handle)
        return papers
    except Exception as e:
        logging.error(f"Error occurred while fetching PubMed details: {e}")
        return None

def main():
    try:
        
        disease_articles = {}

        all_diseases = set()
        for disease_name, diseases in diseases_dict.items():
            for disease in diseases:
                all_diseases.add(disease['name'])

        for disease in all_diseases:
            if disease in disease_articles and disease_articles[disease] != []:
                continue    
            query = f'{disease}'
            disease_articles[disease] = search_pubmed(query, 50)

        with open('disease_articles.json', 'w') as f:
            json.dump(disease_articles, f)
            
    except Exception as e:
        logging.error(f"Error occurred in main function: {e}")

if __name__ == "__main__":
# Check if the JSON file already exists
    if os.path.exists('Diseases_list.json'):
        with open('Diseases_list.json', 'r') as f:
            disease_articles = json.load(f)
    else:
        # Run fetch_data.py to generate the JSON
        os.system('python fetch_data.py')

        # Load the generated JSON into diseases_dict
        with open('Diseases_list.json', 'r') as f:
            disease_articles = json.load(f)

        # Update diseases_dict with the loaded JSON
        diseases_dict.update(disease_articles)  

    main()
