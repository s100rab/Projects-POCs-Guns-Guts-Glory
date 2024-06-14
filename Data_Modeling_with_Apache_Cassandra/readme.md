Explaining the process of setting up Cassandra using Docker, interacting with it using Python, and performing data ingestion. This document outlines the blockers, steps, key learnings, potential challenges, and technologies used. It also includes instructions for quickly and simply installing the required technologies.


# Data Ingestion in Cassandra Using Docker and Python

This project demonstrates how to set up Apache Cassandra using Docker, connect to it using Python, and ingest data into Cassandra tables. The process includes creating keyspaces, tables, and inserting data. This guide outlines the steps, key learnings, challenges, and technologies used in this proof of concept (POC).

## Table of Contents
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Python Script for Data Ingestion](#python-script-for-data-ingestion)
- [Key Learnings](#key-learnings)
- [Challenges](#challenges)

## Technologies Used
- Docker
- Apache Cassandra
- Python
- Jupyter Notebook
- Cassandra Python Driver

## Prerequisites
- Docker installed on your machine
- Python installed on your machine
- Jupyter Notebook (optional but recommended)

## Setup Instructions

### Step 1: Pull and Run Cassandra Docker Image

1. Pull the Cassandra Docker image:
   ```sh
   docker pull cassandra:latest
   ```

2. Run the Cassandra container with port forwarding:
   ```sh
   docker run --name my-cassandra-container -d -p 9042:9042 cassandra:latest
   ```

### Step 2: Connect to Cassandra Using `cqlsh`

1. Use the `cqlsh` command-line tool from within a Docker container to connect to your Cassandra instance:
   ```sh
   docker run -it --network container:my-cassandra-container cassandra:latest cqlsh
   ```

2. Create a keyspace and a table:
   ```sql
   CREATE KEYSPACE test_keyspace WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
   USE test_keyspace;

   CREATE TABLE dummy_table (
       id UUID PRIMARY KEY,
       name text,
       age int
   );
   ```

### Step 3: Install Python Cassandra Driver

1. Install the Cassandra driver for Python:
   ```sh
   pip install cassandra-driver
   ```

### Step 4: Connect to Cassandra via Python and Insert Data

1. Create a Python script `insert_dummy_data.py` with the following content:

   ```python
   from cassandra.cluster import Cluster
   from cassandra.query import SimpleStatement
   import uuid

   # Define the contact points and port
   contact_points = ['127.0.0.1']
   port = 9042

   # Connect to Cassandra
   cluster = Cluster(contact_points, port=port)
   session = cluster.connect()

   # Use the keyspace
   session.set_keyspace('test_keyspace')

   # Insert data into the table
   insert_query = SimpleStatement("""
       INSERT INTO dummy_table (id, name, age) VALUES (%s, %s, %s)
   """)

   # Generate dummy data
   data = [
       (uuid.uuid4(), 'John Doe', 30),
       (uuid.uuid4(), 'Jane Doe', 25),
       (uuid.uuid4(), 'Alice', 28),
       (uuid.uuid4(), 'Bob', 22)
   ]

   for item in data:
       session.execute(insert_query, item)

   print("Data inserted successfully")

   # Close the connection
   cluster.shutdown()
   ```

2. Run the script to insert data:
   ```sh
   python insert_dummy_data.py
   ```

### Step 5: Verify Data Insertion Using `cqlsh`

1. Connect to Cassandra using `cqlsh` and verify the inserted data:
   ```sh
   docker run -it --network container:my-cassandra-container cassandra:latest cqlsh
   ```

2. Execute the following commands in `cqlsh`:
   ```sql
   USE test_keyspace;
   SELECT * FROM dummy_table;
   ```

## Key Learnings
- Setting up Cassandra in a Docker container simplifies the installation and configuration process.
- Using `cqlsh` within Docker allows direct interaction with the Cassandra instance for quick testing and setup.
- The Cassandra Python driver enables programmatic interaction with the database, allowing for complex operations and data manipulation.

## Challenges
- Ensuring the Docker container is correctly configured and running to avoid connection issues.
- Handling exceptions and retry logic when establishing connections to the Cassandra instance.
- Properly formatting and preparing data for insertion into Cassandra tables.

## Conclusion
This project showcases a straightforward way to set up and use Cassandra with Docker and Python. By following the provided steps, you can quickly get a Cassandra instance running, interact with it using `cqlsh`, and perform data operations using Python. This POC serves as a foundation for more complex data modeling and ingestion tasks in Cassandra.
```

You can copy this text into a `README.md` file to showcase your project and guide users through the process of setting up and using Cassandra for data ingestion with Docker and Python.