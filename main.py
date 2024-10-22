import uuid
import json
import datetime

from fastapi import FastAPI, Response, status
app = FastAPI(
    title="Library API (Tanner Folkman)",
    description="API to keep track of your library."
)

#---
#Each author should have the following properties:
#- name
#- bio
#----
class author:

    def __init__(self, name, bio):
        self.name = name
        self.bio = bio
        self.id = str(uuid.uuid4())

#Each book should have the following properties:
#- title
#- description
#- author
#- published date
#---
class book:

    def __init__(self, title, description, author_id, publication_date):
        self.title = title
        self.description = description
        self.author_id = author_id
        self.publication_date = publication_date
        self.id = str(uuid.uuid4())

# -------------------
# Globals
gAuthors = {}
gBooks = {}
# -------------------

#--------------------
#functions

def getJsonAllAuthors():
    jsonDumps = []
    for authorId in gAuthors:
        jsonDumps.append(json.dumps(gAuthors[authorId].__dict__))
    return jsonDumps

def getJsonAllBooks():
    jsonDumps = []
    for bookId in gBooks:
        jsonDumps.append(json.dumps(gBooks[bookId].__dict__))
    return jsonDumps

def validatePublishedDate(published_date):
    res = True

    #isoformat: YYYY-MM-DD
    try:
        datetime.date.fromisoformat(published_date)
    except ValueError:
        res = False

    return res

#---------------------

#---------------------
# Author endpoints

# Create a new author
@app.post("/authors", tags=["Authors"], responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "name": "Tanner", "bio": "Good author", "id": "8739dc13-b849-46ba-8e4b-7918c84ccfbd"
                    }
                }
            },
        },
        400: {
            "description": "Could not create author.",
        }
    })
async def create_author(name: str, bio: str, response: Response):
    newAuthor = author(name, bio)
    if (newAuthor and newAuthor.id):
        gAuthors[newAuthor.id] = newAuthor
        return json.dumps(newAuthor.__dict__)
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return

# Retrieve a list of all authors
@app.get("/authors", tags=["Authors"], responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {"name": "Tanner", "bio": "Good author", "id": "cfb71a37-12e2-4738-ba1d-5595465c57cb"},
                        {"name": "Katie", "bio": "Really good author", "id": "13078732-437b-4489-8d37-08a2ac906d9f"}
                    ]
                }
            },
        }
    })
async def get_authors():
    return getJsonAllAuthors()

# Retrieve a specific author by ID
@app.get("/authors/{author_id}", tags=["Authors"], responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "name": "Tanner", "bio": "Good author", "id": "8739dc13-b849-46ba-8e4b-7918c84ccfbd"
                    }
                }
            },
        },
        400: {
            "description": "Could not find author associated with passed in Id",
        }
    })
async def get_author(author_id: str, response: Response):
    if author_id in gAuthors:
        return json.dumps(gAuthors[author_id].__dict__)
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return 

# Update an author
@app.put("/authors/{author_id}", tags=["Authors"], responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "name": "Tanner", "bio": "Updated Bio", "id": "8739dc13-b849-46ba-8e4b-7918c84ccfbd"
                    }
                }
            },
        },
        400: {
            "description": "Could not find author associated with passed in Id",
        }
    })
async def update_author(author_id: str, name: str, bio: str, response: Response):
    if author_id in gAuthors:
        authorToUpdate = gAuthors[author_id]
        if (authorToUpdate):
            authorToUpdate.name = name
            authorToUpdate.bio = bio

            return json.dumps(authorToUpdate.__dict__)
    
    response.status_code = status.HTTP_400_BAD_REQUEST
    return
        
# Delete an author
@app.delete("/authors/{author_id}", tags=["Authors"], responses={
        200: {
            "description": "Author removed or did not exist",
            "content": None
        }
    })
async def delete_author(author_id: str):
    if author_id in gAuthors:
        del gAuthors[author_id]
    return
#----------------------

# -----------------------
# Book endpoints

# Create a new book
@app.post("/books", tags=["Books"], responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "title": "Book", "description": "Good Book", "author_id": "13078732-437b-4489-8d37-08a2ac906d9f", \
                        "publication_date": "1996-12-21", "id": "a24779d2-71f5-4a37-995c-039171cd35e9"
                    }
                }
            },
        },
        400: {
            "description": "Could not create Book. Either the author_id passed in does not exist or the publication_date passed in is not in iso format YYYY-MM-DD",
        }
    })
async def create_book(title: str, description: str, author_id: str, published_date: str, response: Response):
    if author_id in gAuthors:
        if (validatePublishedDate(published_date)):
            newBook = book(title, description, author_id, published_date)
            if (newBook and newBook.id):
                gBooks[newBook.id] = newBook
                return json.dumps(newBook.__dict__)
        
    response.status_code = status.HTTP_400_BAD_REQUEST
    return

# Retrieve a list of all books
@app.get("/books", tags=["Books"], responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {"title": "My Life", "description": "Good Book", "author_id": "13078732-437b-4489-8d37-08a2ac906d9f", \
                        "publication_date": "1996-12-21", "id": "a24779d2-71f5-4a37-995c-039171cd35e9"},
                        {"title": "Computer Science 101", "description": "For Programers", "author_id": "08929290-cf2a-4e6a-960a-7c686a43c3f6", \
                        "publication_date": "1996-12-21", "id": "06fab38c-8a2a-460c-a9aa-8a5a62a337d4"}
                    ]
                }
            },
        }
    })
async def get_books():
    return getJsonAllBooks()

# Retrieve a specific book by ID
@app.get("/books/{book_id}", tags=["Books"], responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "title": "My Life", "description": "Good Book", "author_id": "13078732-437b-4489-8d37-08a2ac906d9f", \
                        "publication_date": "1996-12-21", "id": "a24779d2-71f5-4a37-995c-039171cd35e9"
                    }
                }
            },
        },
        400: {
            "description": "Could not find book associated with passed in Id",
        }
    })
async def get_book(book_id: str, response: Response):
    if book_id in gBooks:
        return json.dumps(gBooks[book_id].__dict__)
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return 

# Update a book
@app.put("/books/{book_id}", tags=["Books"], responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "title": "My Life", "description": "Updated to Really Good Book", "author_id": "13078732-437b-4489-8d37-08a2ac906d9f", \
                        "publication_date": "1996-12-21", "id": "a24779d2-71f5-4a37-995c-039171cd35e9"
                    }
                }
            },
        },
        400: {
            "description": "Could not create Book. Either the author_id passed in does not exist or the publication_date passed in is not in iso format YYYY-MM-DD",
        }
    })
async def update_book(book_id: str, title: str, description: str, author_id: str, published_date: str, response: Response):
    if book_id in gBooks:
        bookToUpdate = gBooks[book_id]
        if (bookToUpdate and validatePublishedDate(published_date)):
            if author_id in gAuthors:
                bookToUpdate.title = title
                bookToUpdate.description = description
                bookToUpdate.author_id = author_id
                bookToUpdate.published_date = published_date

                return json.dumps(bookToUpdate.__dict__)
    
    response.status_code = status.HTTP_400_BAD_REQUEST
    return

# Delete a book
@app.delete("/books/{book_id}", tags=["Books"], responses={
        200: {
            "description": "Book removed or did not exist",
            "content": None
        }
    })
async def delete_book(book_id: str):
    if book_id in gBooks:
        del gBooks[book_id]
    return
#----------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)