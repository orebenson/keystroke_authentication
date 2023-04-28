from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime


from . import schemas, models
from .database import SessionLocal, engine
from .matching import get_match

models.BaseModel.metadata.create_all(bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=['https://users.sussex.ac.uk', '139.184.223.130'],
	allow_methods=['POST'],
	allow_headers=['*']
)

@app.get('/')
async def hello():
	return {"message": "Hello World"}

@app.post('/sample/')
async def sample(request: schemas.Request, session: Session = Depends(get_db)) -> schemas.Response:
	print(request)

	username = request.username
	password = request.password
	keytimes = request.keytimes
	train = request.train

	user = session.query(models.User).filter(models.User.username == username).first()

	if user and password != user.password:
		return schemas.Response(
			status='bad',
			message='Username and password did not match'
		)

	if train:
		if not user:
			user = models.User(username=username, password=password)
			session.add(user)
			session.commit()
			session.refresh(user)

		sample = models.Sample(user_id=user.id, timestamp=datetime.now(), keytimes=keytimes)
		session.add(sample)
		session.commit()

		return schemas.Response(
			status='good',
			message='Training data submitted'
		)
		
	else:
		if not user:
			return schemas.Response(
				status='bad',
				message='User does not exist'
			)

		# RUN MATCHING ALGORITHM
		match = get_match(keytimes, user)

		if match:
			return schemas.Response(
				status='good',
				message='Input matched'
			)
		else:
			return schemas.Response(
				status='bad',
				message='Input did not match'
			)

	return schemas.Response(
		status='bad',
		message='You werent supposed to see this'
	)




