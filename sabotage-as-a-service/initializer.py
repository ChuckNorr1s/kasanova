from context import create_vector_db
from poetry_dir.plugins import new_heresy_vectors, data_weaponizer, heresy_vectors, chrome_vectors_location, init_more_heresies
from site_scraper import add_heresy_vectors

pdf_file = heresy_vectors  # Replace with your actual PDF file path
persist_directory = chrome_vectors_location  # Directory where the vector DB will be stored

# Create the vector database from the PDF file
create_vector_db(pdf_file, persist_directory)

# Add heresy vectors (optional)
if init_more_heresies:
    add_heresy_vectors(new_heresy_vectors, persist_directory)
    add_heresy_vectors(data_weaponizer, persist_directory)