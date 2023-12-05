# Vector Embedding Application

## Introduction
This application, built with Streamlit, processes text files by converting them to vector embeddings using FAISS for efficient similarity search. Users can upload files, query the processed data, and the application ensures that data is managed in-memory without persistent storage.


## Features
- File upload and processing
- Conversion of text data into vector embeddings
- In-memory storage of embeddings using FAISS
- Efficient querying of vector data
- Non-persistent data management (data not stored across sessions)

## Installation

To set up the project locally, follow these steps:

### Prerequisites
- Ensure you have Python 3.11 installed on your system.
- Install Pipenv, which is used for managing project dependencies. You can install it using pip:

  ```bash
  pip install pipenv
  ```
- Clone the repository
  ```bash
  git clone https://github.com/yourusername/your-repo-name.git
  ```
- Navigate to the repository directory
  ```bash
  cd your-repo-name
  ``
- Install dependencies using Pipenv
  ```bash
  pipenv install
  ```
- Activate the Pipenv environment
  ```bash
  pipenv shell
  ```

- Run the application (modify this command as per your application's entry point)

  ```bash
  streamlit run app.py
  ```

