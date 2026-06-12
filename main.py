from fastapi import FastAPI , Depends , HTTPException, Query
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models,schemas
from auth import create_token,verify_token



models.Base.metadata.create_all(bind=engine) #creates table

app=FastAPI()

#DB DEPENDANCY

def get_db():  # It creates a connection, shares it, and guarantees it closes when done.
    db=SessionLocal()
    try :
        yield db
    finally :
        db.close()
           
#Login API
@app.post("/login")
def login():
    return{
        "access_token": create_token({"user":"admin"}),
        "token_type": "bearer"
    }
 
#Home route
@app.get("/")
def home():
    return{
        "message": "Blog API started"
    }    
    
#create Blog-protected

@app.post("/blogs", response_model=schemas.BlogResponse)
def create_blog(blog: schemas.BlogCreate,db : Session=Depends(get_db), user=Depends(verify_token)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#Read all blog
@app.get("/allblogs")

def read_blogs(page:int=1.,
               limit:int=5,
               search:str=Query(default=""),
               db:Session=Depends(get_db)):
    query = db.query(models.Blog)
    if search:
        query=query.filter(models.Blog.title.ilike(f"%{search}%"))
    total = query.count()
    start=(page-1)*limit
    blogs=query.offset(start).limit(limit).all()
    return{
        "page":page ,
        "limit": limit,
        "total": total,
        "data": blogs
    }

#Read one blog

@app.get("/allblogs/{id}", response_model=schemas.BlogResponse)
def show_blog(id:int,db:Session=Depends(get_db)):

    blog=db.query(models.Blog).filter(models.Blog.id==id).first()

    if not blog:
        raise HTTPExecption(status_code=404 , detail = "Blog Not found")
    return blog    


#Update blog-protected

@app.put("/allblogs/{id}", response_model=schemas.BlogResponse)

def update_blog(id:int,blog: schemas.BlogCreate,db:Session=Depends(get_db),user=Depends(verify_token)):

    existing_blog=db.query(models.Blog).filter(models.Blog.id==id).first()

    if not existing_blog:
        raise HTTPException(status_code=404 , detail = "Blog Not found")
    existing_blog.title=blog.title
    existing_blog.content=blog.content
    db.commit()
    db.refresh(existing_blog)  # Added: Refreshes the database state for the response model
    return existing_blog    

#DELETE BLOG
@app.delete("/allblogs/{id}")

def delete_blog(id:int , db:Session=Depends(get_db)):

    blog= db.query(models.Blog).filter(models.Blog.id==id)

    if not blog.first():
        raise HTTPExecption(status_code=404 , detail = "Blog Not found")
    blog.delete()
    db.commit()
    return{
        "message":"Blog deleted "
    }    




 



