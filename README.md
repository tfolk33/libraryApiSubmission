# libraryApiSubmission
Hey y'all! Thanks for this opportunity to demonstrate my ability through this coding assignment. I really enjoyed working on it and I hope you can review it without any issues. Here are the details.

# Implementation Details
I chose to implement this API using the FastAPI webframework with Python. I chose this framework for its fast processing, built-in parameter validation, error handling, and ease of testing.

I have implemented 10 API routes that correspond directly with the 10 operations named in the instructions.

The design is centered around two custom classes: Authors and Books. Each is designed after the description provided. When an Author or Book object is created, a unique ID will be assigned to that object. Books are linked to Authors through the class parameter "author_id." The ID of the Author who wrote the Book must be passed in when the Book is created, or it will fail.

Authors and Books are stored in their respective global dictionaries: gAuthors and gBooks. As the API calls are made, these dictionaries are updated accordingly. I chose to use dictionaries because they can "map" an id to an object very well. I used the id of the Author and Books as the "key" of the dictionaries and the Objects themselves as the "value". This allowed me to take advantage of the standard functions of a dictionary to optimize the CRUD operations.

# How to Run
In an effort to avoid any issues with the environment, I have packaged the Python file and all dependencies into a stand-alone executable located at: .\dist\main.exe.

To run:
- Download .\dist\main.exe
- Run the exe
- The server will now be taking requests at http://localhost:8000/

You can also run "py main.py" if you have Python installed, but you may need to download some packages.

# API Documentation
After the server is running you will find the API Documentation at http://localhost:8000/docs
When you select the down arrow on the right side of any API route, there will be two sections - parameters and possible HTTP responses.

# Testing
You can test the API in anyway that you prefer to send HTTP requests (Postman, Curl, etc). Additionally, there is an option to test the API at http://localhost:8000/docs. When you select the dropdown for an endpoint on that page, there will be a button in the top right corner that says "try it out". When you press that, you can adjust the paramters above and then press the blue "Execute" button and the request will be sent.

Some testing tips specific to my implementation:
- A book's publication date must be in iso format: YYYY-MM-DD
- A book's author_id must be an id of an author already added to the server.

# Tools Used
There are a few python packages that I utilized in my implementation:
- "UUID" to generate unique ids.
- "json" to return book and author objects as json.
- "datetime" to validate published date.

I used Postman to test the server.

I used ChatGPT to generate the api route stubs, so I could speed up that task. You can view the prompt and results in the included text file "AI_Prompt_Result.txt"
