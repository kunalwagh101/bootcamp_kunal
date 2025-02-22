from fastapi import FastAPI, Request ,HTTPException ,Depends,BackgroundTasks
from fastapi.responses import HTMLResponse ,RedirectResponse ,FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing  import Optional,List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
app = FastAPI()
templates = Jinja2Templates(directory="templates")
import logging
logger = logging.getLogger("uvicorn")
app.state.items = {} 
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from pathlib import Path
from database import SessionLocal, engine
import  models 
from models import CarModel

models.Base.metadata.create_all(bind=engine)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

"""
No.4 Request Body and Pydantic Models

Objective: Define and use Pydantic models to validate and structure request data.
Task: Create a Pydantic model for items and use it in a route to add a new item.
Expected Output: Validation and addition of items through the Pydantic model.
"""

class Cars(BaseModel):

    name :Optional[str] = None
    company : str
    model : Optional[str] =None
    color  : Optional[str] =None

    class Config:
        orm_mode = True


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

"""              CREATE           """
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


"""              Read           """

@app.get("/test/read",response_class = HTMLResponse)
def test_read(request:Request):

    if "item" not in request.session:
        raise HTTPException(status_code=404, detail="No item in session")
    info =  request.session["item"]
    for key  in  request.session.keys():
        val = request.session[key]
        logger.info(f"entrys :{val}")
   
    return HTMLResponse(f"<h4>{request.session.keys()}</h4>")

"""              Update         """

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
    
"""              delete             """

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
    Audi = Cars( name = "A4",company = "audi" ,model="51",color = "red")
    item = CarModel(**Audi.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    logger.info(f"{Audi} -{item} ")
    message = f"New car added successfully: {Audi.company}"
    
    redirect_url = f"/?value={message.replace(' ', '+')}"
    return RedirectResponse(url=redirect_url, status_code=303)

@app.get("/read",response_class=HTMLResponse )
def read(request : Request ,db :Session = Depends(get_db)) :
  
    # get_value  = db.query(models.CarModel).offset(0).limit(10).all()
    get_value  = db.query(CarModel).all()
    if not get_value :
        return HTMLResponse(f"<h3>nothing actually exits yet</h3>")
    car =  get_value[0]
    logger.info(f"get_value = {car} - {car.id}", )
    return HTMLResponse(f"this is the value in db  : {get_value[0]}")
 

@app.get("/read/{name}" , response_class=HTMLResponse)
def read_value(request :Request,name :Optional[str] ,db :Session = Depends(get_db), id:Optional[int] =None ):
    if not id :
         get_value  =  db.query(CarModel).filter(CarModel.name == name).first()
    else :
        get_value  =  db.query(CarModel).filter(CarModel.name == name ,CarModel.id == id).first()
       
    if not get_value :
        return  HTMLResponse(f"<h3> Requested info did not found ! </h3>")

    return HTMLResponse(f"<h3>your Requested info is this = {get_value}  </h3>")

@app.get("/update/{id}" , response_class=HTMLResponse)
def update(request:Request,id :int,model :Optional[str] = None ,name:Optional[str] = None ,
           db:Session = Depends(get_db)):
    if not id :
        return HTMLResponse(f"id is not available")
    query  =  db.query(CarModel).filter(CarModel.id  ==  id ).first()
    if not query :
        return HTMLResponse(f'Oops item does not exits ')
    if not (model or name):
        query.color = "changed"
    else:
        if model:
            query.model = model
        if name:
            query.name = name

    db.commit()
    db.refresh(query)
    return HTMLResponse(f'This your item = {query}')
    
@app.get("/delete/{id}", response_class =HTMLResponse )
def delete(request:Request,id : int,db : Session= Depends(get_db)):
    if not id :
        return HTMLResponse(f"please enter the id ")
    query =  db.query(CarModel).filter(CarModel.id == id).first()
    if not query:
        return HTMLResponse(f"Oops item does not exists !")
    db.delete(query)
    db.commit()
    message = f"deleted {query.name} succesfully "
    redirect_url  = f"/?value ={message.replace(' ', '+')}" 
    return RedirectResponse(url= redirect_url ,status_code=303)

"""
No.6 Background Tasks

Objective: Utilize background tasks in FastAPI to perform operations after returning a response.
Task: Implement a route that initiates a background task for sending an email notification upon completing a certain action.
Expected Output: Email notification is sent as a background task.

"""

def send_email_notification(email: str, subject: str, body: str):
   
    print(f"Sending email to: {email}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")

@app.post("/do-action")
def do_action(background_tasks: BackgroundTasks, email: str):
    subject = "Action Completed"
    body = "Your action has been successfully completed!"   
    background_tasks.add_task(send_email_notification, email, subject, body) 
    return JSONResponse({"message": "Action initiated. An email notification will be sent shortly."})

"""
No.7 File Uploads

Objective: Handle file uploads in FastAPI.
Task: Create a route that allows users to upload files, and save them to a specific directory.
Expected Output: Uploaded files are saved to the server.
"""

@app.get("/uploads" ,response_class=HTMLResponse)
async def list_uploads(request: Request):
    file = Path.cwd()/"content.txt"
    if not file.exists() :
        return HTMLResponse(f" file not found")
    storage_file =  Path.cwd()/"output"
    storage_file.mkdir(parents = True , exist_ok = True)
  
    try :
        input_file  =  storage_file / "output.txt"
        if not input_file.exists():
            logger.info(f"does not exits ")

        with file.open("r", encoding="utf-8") as infile:
            content = infile.read()
        with open(input_file, "w", encoding="utf-8") as outfile:
            outfile.write(content)
    except Exception as e :
        logger.info(f" error occoure {e}")
        return HTMLResponse(f" Oops somthing went wrong {e} !")


    return HTMLResponse(f"this is a file {file}")


"""
No.8 Serving Static Files

Objective: Serve static files, such as images or HTML files, with FastAPI.
Task: Configure FastAPI to serve static files from a directory.
Expected Output: Static files are accessible via FastAPI. API routes take precedence.

"""
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/image", response_class=HTMLResponse)
async def image():
    return HTMLResponse("<h1>Welcome to the FastAPI Application</h1><p>Visit <a href='/show-image'> image</a> to see the image.</p>")


@app.get("/show-image", response_class=FileResponse)
def send_image():
  
    image_path = "static/tojo.jpg"
    return FileResponse(image_path, media_type="image/jpeg")