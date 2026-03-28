from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, auth, database, os, shutil

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="Gallery App - Tran Thi Kim Ngan")

# Cho phép Live Server (port 5500) truy cập
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

if not os.path.exists("uploads"): os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.post("/register")
def register(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    hashed = auth.get_password_hash(password)
    user = models.User(username=username, email=email, password=hashed)
    db.add(user); db.commit(); return {"msg": "Đăng ký xong"}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    # Tìm user chỉ bằng username và password thuần túy
    user = db.query(models.User).filter(models.User.username == username, models.User.password == password).first()
    if not user: 
        raise HTTPException(400, "Sai tài khoản")
    
    # Trả về kết quả luôn, không cần token phức tạp cho máy trường
    return {"token": "fake-token-ngan-123", "username": user.username}
@app.post("/photos")
def upload(title: str = Form(...), desc: str = Form(None), file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    path = f"uploads/{file.filename}"
    with open(path, "wb") as b: shutil.copyfileobj(file.file, b)
    photo = models.Photo(title=title, description=desc, image_url=path, user_id=1)
    db.add(photo); db.commit(); return {"msg": "Upload thành công"}

@app.get("/photos")
def get_all(q: str = None, db: Session = Depends(database.get_db)):
    query = db.query(models.Photo)
    if q: query = query.filter(models.Photo.title.contains(q))
    return query.all()

@app.delete("/photos/{id}")
def delete(id: int, db: Session = Depends(database.get_db)):
    p = db.query(models.Photo).filter(models.Photo.id == id).first()
    db.delete(p); db.commit(); return {"msg": "Xóa xong"}