from fastapi import FastAPI, Request ,HTTPException ,Depends
from fastapi.responses import HTMLResponse ,RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing  import Optional,List
app = FastAPI()
templates = Jinja2Templates(directory="templates")
import logging
logger = logging.getLogger("uvicorn")
app.state.items = {} 
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

from database import SessionLocal, engine
import  models 

models.Base.metadata.create_all(bind=engine)


"""
No.4 Request Body and Pydantic Models

Objective: Define and use Pydantic models to validate and structure request data.
Task: Create a Pydantic model for items and use it in a route to add a new item.
Expected Output: Validation and addition of items through the Pydantic model.
"""


class Cars(BaseModel):
    id : int
    company : str
    model : Optional[str] =None
    color  : Optional[str] =None

    class Config:
        orm_mode = True


"""
No.5 
Database Integration

Objective: Integrate a simple database (e.g., SQLite) with FastAPI for persisting data.
Task: Connect FastAPI to a SQLite database and modify CRUD operations to use the database.
Expected Output: CRUD operations interact with a SQLite database. (To add, update, and delete items),
"""


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/create", response_class=HTMLResponse)
def create(request : Request ,db:Session = Depends(get_db),):
    Audi = Cars( id = 1 ,company = "audi" ,color = "red")
    item = models.CarModel(**Audi.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    logger.info(f"{Audi} -{item} ")
    message = f"New car added successfully: {Audi.company}"
    
    redirect_url = f"/?value={message.replace(' ', '+')}"
    return RedirectResponse(url=redirect_url, status_code=303)

@app.get("/read",response_class=HTMLResponse )
def read(request : Request ,db :Session = Depends(get_db)) :
    get_value  = db.query(models.CarModel).offset(0).limit(10).all()
    if get_value :
        car =  get_value[0]
        logger.info(f"get_value = {car} - {car.id}", )
        return HTMLResponse(f"this is the value in db  : {get_value[0]}")
    return HTTPException(f"somthig went wrong") 


# @app.get()
# def read_value(request : Request,name db:Session = Depends(get_db)):



"""
No.1 hello World API

Objective: Create a basic FastAPI app that returns "Hello, World!" on the root path.
Task: Initialize a FastAPI application and define a route that responds with "Hello, World!".
Expected Output: Accessing the root URL displays "Hello, World!".
"""

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
        value = request.query_params.get("value", "")
        items = ["Mercs", "bmw", "audi", "ford"]
        return templates.TemplateResponse("index.html", {"request": request, "items": items, "value": value})




"""
No.2 CRUD Operations for a Resource

Objective: Implement CRUD operations for a resource (e.g., items) using FastAPI.
Task: Define routes for creating, reading, updating, and deleting items, using an in-memory structure to store them.
Expected Output: Functional CRUD operations for items.
"""




@app.get("/test/create",response_class=HTMLResponse)
def test_create(request:Request):
    item  =  Cars(id = "1",company = "bwm" , model = "5", color = "red" )  
    if "item" in app.state.items.keys():
        raise HTTPException(status_code=400, detail="Item already exists")
    request.session["item"] = item.model_dump()
    app.state.items["item"] = item
    val =   request.session["item"]
    print("session = ", request.session)
    return f"{item} , session ={ val} stored succesfull "

@app.get("/test/read",response_class = HTMLResponse)
def test_read(request:Request):

    if "item" not in request.session:
        raise HTTPException(status_code=404, detail="No item in session")
    info =  request.session["item"]
    for key  in  request.session.keys():
        val = request.session[key]
        logger.info(f"entrys :{val}")
   
    return HTMLResponse(f"<h4>{request.session.keys()}</h4>")


@app.get("/test/update" ,response_class = HTMLResponse)
def test_update(request : Request):
    try :
        new_item  = Cars(company = "Audi" , model="A" ,color= "white") 
        request.session["item"] = new_item.model_dump()
        val = request.session["item"]
        return HTMLResponse(f"<h4>{val} updated succesfull </h4>")
    except Exception as e :
        logger(f"{e} this is the error ")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/test/delete/{value}",response_class = HTMLResponse)
def test_delete(request: Request,value:str) :
    if value not in request.session.keys():
      raise HTTPException(status_code=404, detail="No item in session")
    del request.session[value]

    return  HTMLResponse(f"<h4>Item deleted successfully</h4>")




"""
No.3 Path and Query Parameters

Objective: Use path and query parameters in FastAPI routes.
Task: Create a route that accepts path parameters for a resource ID and optional query parameters for filtering results.
Expected Output: A route that dynamically responds based on provided parameters.
"""

@app.get("/add/{value}" , response_class = HTMLResponse )
def path_work(request : Request ,
               value:str ,
               company : Optional[str]= None,
               model : Optional[str]= None ,
               color : Optional[str]= None) :
    
    if value not in  request.session.keys() :
        request.session[value] = Cars( company = company , model = model , color= color ).model_dump()
        info = request.session[value]
        return HTMLResponse(f"<h1> New value {value} created! and {info}  </h1>")
    if company :
     print("name =", request.session[value]["company"])
     if company == request.session[value]["company"] :      
        return HTMLResponse("<h1>value all read exit</h1> ")
    

        

