from fastapi import FastAPI, Request,Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI()

templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
   
    valid_username = "admin"
    valid_password = "secret"

   
    is_valid_username = secrets.compare_digest(credentials.username, valid_username)
    is_valid_password = secrets.compare_digest(credentials.password, valid_password)

    if not (is_valid_username and is_valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username





@app.get("/",response_class=HTMLResponse)
async def main(request : Request):
    lists = ["apple" ,"mango" ,"pinapple" ,"orange"]
    
    return templates.TemplateResponse("index.html",{"request":request, "lists" :lists})




@app.get("/protected")
def read_protected(username: str = Depends(get_current_username)):
    return {"message": f"Hello, {username}! You have access to this secure route."}