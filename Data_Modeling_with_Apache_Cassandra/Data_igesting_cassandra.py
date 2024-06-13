# %% [markdown]
# # Part I. ETL Pipeline for Pre-Processing the Files

# %% [markdown]
# #### Import Python packages 

# %%
import numpy as np

# %%
# Import Python packages 
import pandas as pd
import cassandra
import re
import os
import glob
import numpy as np
import json
import csv

# %% [markdown]
# #### Creating list of filepaths to process original event csv data files

# %%
# checking current working directory
print(f"Current working directory : {os.getcwd()}")

# Get current folder and subfolder event data
filepath = os.getcwd() + '/event_data'

# Create a list of files and collect each filepath
for root, dirs, files in os.walk(filepath):
    
# join the file path and roots with the subdirectories using glob
    file_path_list = glob.glob(os.path.join(root,'*'))
    #print(file_path_list)

# %% [markdown]
# #### Processing the files to create the data file csv that will be used for Apache Casssandra tables

# %%
# initiating an empty list of rows that will be generated from each file
full_data_rows_list = [] 
    
# for every filepath in the file path list 
for f in file_path_list:

# reading csv file 
    with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
        # creating a csv reader object 
        csvreader = csv.reader(csvfile) 
        next(csvreader)
        
 # extracting each data row one by one and append it        
        for line in csvreader:
            full_data_rows_list.append(line) 
            

print(f"Total rows : {len(full_data_rows_list)}")
print(f"Sample data:\n {full_data_rows_list[:5]}")

# creating a smaller event data csv file called event_datafile_full csv that will be used to insert data into the \
# Apache Cassandra tables
csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
    writer = csv.writer(f, dialect='myDialect')
    writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',\
                'level','location','sessionId','song','userId'])
    for row in full_data_rows_list:
        if (row[0] == ''):
            continue
        writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))


# %%
# checking the number of rows in new event csv file
with open('event_datafile_new.csv', 'r', encoding = 'utf8') as f:
    print(sum(1 for line in f))

# %% [markdown]
# ## Now we are ready to work with the CSV file titled <font color=red>event_datafile_new.csv</font>, located within the Workspace directory.  The event_datafile_new.csv contains the following columns: 
# - artist 
# - firstName of user
# - gender of user
# - item number in session
# - last name of user
# - length of the song
# - level (paid or free song)
# - location of the user
# - sessionId
# - song title
# - userId
# 
# The image below is a screenshot of what the denormalized data should appear like in the <font color=red>**event_datafile_new.csv**</font> after the code above is run:<br>
# 
# <img src="images/image_event_datafile_new.jpg">

# %% [markdown]
# #### Creating a Cluster

# %%
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# %%
from cassandra.cluster import Cluster

from cassandra.cluster import Cluster
from time import sleep

# Replace with your Cassandra Docker container IP address and port
contact_points = ['127.0.0.1']
port = 9042

try:
    # Attempt to connect with retries
    retry_count = 1
    for attempt in range(retry_count):
        try:
            cluster = Cluster(contact_points, port=port)
            session = cluster.connect()
            print("Connection to Cassandra established!")
            break  # Successful connection, exit retry loop
        except Exception as e:
            print(f"Failed to connect to Cassandra on attempt {attempt + 1}. Retrying...")
            sleep(10)  # Wait for 10 seconds before retrying

    # Add your Cassandra operations here

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the connection
    if cluster:
        cluster.shutdown()



# %%
# This should make a connection to a Cassandra instance your local machine 
# (127.0.0.1)

from cassandra.cluster import Cluster
try:
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    print("Connection Established !!")
except Exception as e:
    print(f"Connection Failed !! Error : {e}")

# %%
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


# %% [markdown]
# #### Creating Keyspace

# %%
keyspace_query = """CREATE KEYSPACE IF NOT EXISTS sparkify 
                    with REPLICATION = 
                    { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
                """

# Creating Keyspace
try:
    session.execute(keyspace_query)
except Exception as e:
    print(f"Failed to create keyspace!! Error : {e}")

# %% [markdown]
# #### Setting Keyspace

# %%
# Setting KEYSPACE to the keyspace specified above
session.set_keyspace('sparkify')

# %% [markdown]
# ### Now we need to create tables to run the following queries. Remember, with Apache Cassandra we model the database tables on the queries we want to run.

# %% [markdown]
# ## Below are the queries following which we will build out data model
# 
# ### 1. Give the artist, song title and song's length in the music app history that was heard during  sessionId = 338, and itemInSession  = 4
# 
# 
# ### 2. Give only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182
#     
# 
# ### 3. Give every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'
# 
# 
# 

# %% [markdown]
# # ========================================================================================================

# %% [markdown]
# ## Query 1 
# 
# ### For query 1, we need a way to run query on sessionId and itemInSession. So, our primary key must have these columns. We can partition the data on sessionId.
# 
# ### Our Select query : SELECT artist, song, length FROM  session_item where sessionId = 338 and itemInSession = 4
# ### Our Primary key will be (sessionId, itemInSession), where sessionId is the partition key and  itemInSession is the clustering column.
# ### Columns we included in the table : 

# %%
# Creating table for query1 
create_query1 = """CREATE TABLE IF NOT EXISTS 
session_item (artist text, song text, length float, sessionId int, itemInSession int, 
PRIMARY KEY (sessionId, itemInSession))"""

try: 
    session.execute(create_query1)
    print("Table Created!!")
except Exception as e:
    print(f"Table creation failed!! Error : {e}")

# %%
# Using the event file
file = 'event_datafile_new.csv'

# Reading csv file and inserting rows into cassandra tables.
with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
        query = "INSERT INTO session_item (artist, song, length, sessionId, itemInSession) "
        query = query + " VALUES (%s, %s, %s, %s, %s) "
        session.execute(query, (line[0], line[10], float(line[5]), int(line[8]), int(line[3])) )

# %% [markdown]
# #### Do a SELECT to verify that the data have been inserted into each table

# %%
# SELECT statement to verify the data was entered into the table
select_query1 = "SELECT artist, song, length FROM  session_item where sessionId = 338 and itemInSession = 4"
try:
    rows = session.execute(select_query1)
except Exception as e:
    print(e)
    
for row in rows:
    print(row)

# %% [markdown]
# ## Query 2
# 
# ### For query 2, we need a way to run query on sessionId and userId. Also, we need the data sorted on itemInSession. So, our primary key must have these columns. We can partition the data on a composite key (sessionId, userId).
# 
# ### Our Select query : SELECT artist, song, firstName, lastName FROM  user_session where sessionId = 182 and userId = 10
# ### Our Primary key will be ((sessionId, userId), itemInSession)), where (sessionId, userId) is the partition key and  itemInSession is the clustering column.
# ### Also, we are using the clause - WITH CLUSTERING ORDER BY (itemInSession ASC), to sort our data based on itemInSession
# ### Columns we included in the table : sessionId, userId, artist, song, firstName, lastName, itemInSession

# %%
# Creating table for query2 
create_query2 = """CREATE TABLE IF NOT EXISTS user_session (sessionId int, userId int, artist text, song text, firstName text, lastName text, itemInSession int, PRIMARY KEY ((sessionId, userId), itemInSession)) WITH CLUSTERING ORDER BY (itemInSession ASC) """

try: 
    session.execute(create_query2)
    print("Table Created!!")
except Exception as e:
    print(f"Table creation failed!! Error : {e}")

# %%
file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
        query = "INSERT INTO user_session (sessionId, userId, artist, song, firstName, lastName, itemInSession) "
        query = query + " VALUES (%s, %s, %s, %s, %s, %s, %s) "
        session.execute(query, (int(line[8]), int(line[10]), line[0], line[9], line[1], line[4], int(line[3])  ) )

# %%
# SELECT statement to verify the data was entered into the table
select_query2 = "SELECT artist, song, firstName, lastName FROM  user_session where sessionId = 182 and userId = 10"
try:
    rows = session.execute(select_query2)
except Exception as e:
    print(e)

for row in rows:
    print(row)

# %% [markdown]
# ## Query 3
# 
# ### For query 3, we need a way to run query on song. So, our primary key must have song. Also, the query should be such that it does not contain duplicate users for a song. So we need to model data in such a way that we don't allow duplicate users for a song in our table. This can be acheived by including userId in our primary key.
# 
# ### Our Select query : SELECT song, firstName, lastName FROM user_song where song = 'All Hands Against His Own'
# ### Our Primary key will be ((song), userId)), where song is the partition key and  userId is the clustering column.
# ### Columns we included in the table : song, userId, firstName, lastName

# %%
# Creating table for query3

create_query3 = """CREATE TABLE IF NOT EXISTS user_song (song text, userId int, firstName text, lastName text, PRIMARY KEY ((song), userId))"""

try: 
    session.execute(create_query3)
    print("Table Created!!")
except Exception as e:
    print(f"Table creation failed!! Error : {e}")

# %%
file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
        query = "INSERT INTO user_song (song, userId, firstName, lastName) "
        query = query + " VALUES (%s, %s, %s, %s) "
        session.execute(query, (  line[9], int(line[10]), line[1], line[4] )  )

# %%
# SELECT statement to verify the data was entered into the table
select_query2 = "SELECT song, firstName, lastName FROM user_song where song = 'All Hands Against His Own'"
try:
    rows = session.execute(select_query2)
except Exception as e:
    print(e)

for row in rows:
    print(row)

# %% [markdown]
# ### Drop the tables before closing out the sessions

# %%
session.execute("DROP TABLE IF EXISTS sparkify.session_item")
session.execute("DROP TABLE IF EXISTS sparkify.user_session")
session.execute("DROP TABLE IF EXISTS sparkify.user_song")

# %% [markdown]
# ### Close the session and cluster connection¶

# %%
session.shutdown()
cluster.shutdown()

# %%