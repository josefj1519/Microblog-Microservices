CPSC 449-01
Project 2: Microblog Microservices
William Timani: williamtimani@csu.fullerton.edu
Josef Jankowski: josefj1519@csu.fullerton.edu

Description:
This project utilizes Flask, Pugsql and Foreman among other libraries in order to provide microservices for a simple blog-type web service. 
Features include: creating a user, authenticating, following/unfollowing, posting a tweet and checking timelines containing user's recent tweets. 
For details on how to initialize the database and use these services, see below. 

Contents:
queries
	timeline_queries.sql
	users_queries.sql
.env
Procfile
README.txt
REST_API_Documentaiton.pdf
api.cfg
schema.sql
timelines.py
users.py

Database Initialization:
In order to intialize the database, ensure you have extracted the contents of the compressed file into a single folder, perserving the directory structure. 
In the terminal, navigate to the root folder with the extracted contents and execute the command: FLASK_APP=users flask init. 
The database will be initialized with data entries and the services are ready to be used.

Starting The Services:
To start the services, in the terminal, navigate to the root folder with the extracted contents of the project. 
Execute the command: foreman start and leave this terminal window running for as long as the services need to be active for. 
In order to make a request to the services, execute an http request with the desired resource (check REST_API_Documentation for resource names or .py files for sample invocation lines for each function). 
Example request to post a tweet using an HTTPie command: http POST http://127.0.0.1:<PORT>/tweet/create user='' text=''.

