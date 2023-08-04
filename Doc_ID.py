import pandas as pd
import re

def extract_document_id(url):
    # Use regular expressions to extract the document ID from the URL
    
    #match = re.search(r'/document/d/([a-zA-Z0-9_-]+)/', url)
    #match = re.search(r'/document/d/([^/]+)/', url)
    match = re.search(r"\bd/\w+", url)
    if match:
        return match.group()[2:]
    else:
        return None
    
def main():
    csv_file = r"C:\Users\sneha\Desktop\All\PulseLabs\BWS - Week 1.csv"
    df = pd.read_csv(csv_file)
    df.iloc[:, 1] = df.iloc[:, 1].astype(str)
    urls = df.iloc[:,1]
    document_ids = []

    for url in urls:
        doc_id = extract_document_id(url)
        if doc_id:
            document_ids.append(doc_id)
        else:
            document_ids.append('0')

    df['Document_ID'] = document_ids
    df.to_csv(csv_file, index=False)
    print(f'The document IDs have been added to the third column of "{csv_file}".')

if __name__ == '__main__':
    main()