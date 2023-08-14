Step-by-Step Workflow:

1. URL Extraction and Preprocessing:
-Use the 'extract_urls.ipynb' notebook to extract URLs from the main target website.
-Process these URLs to remove any duplicates or irrelevant entries.
-Save the cleaned URLs to a file named 'urls.txt'.

2.API Key Configuration:
-Obtain an API key from OpenAI.
-Save this key in the file named 'apikey.py'.

3. Data Processing and Embedding:
- Use the 'main.ipynb' notebook to execute the following steps:
Step 1: Load URLs from the 'urls.txt' file.
Step 2: Fetch data from the URLs and save the data locally on the hard disk.
Step 3: Split the data into individual documents of a specific chunck size.
Step 4: Embed these documents into a FAISS database and save this database locally on the hard disk.
Step 5: To minimize errors, embed the documents in batches. Save each batch to a separate database. After embedding all batches, merge them into a single consolidated database.

4. Running the App
- Ensure that the database, the apikey.py file, and the app.py file are all saved in the same directory.
- Open your terminal.
- Execute the command: streamlit run app.py.
- Enjoy using the app!
