from pydantic import BaseModel
from typing import List

class Request(BaseModel):
	username: str
	password: str
	keytimes: List[float]
	train: bool

class Response(BaseModel):
	status: str
	message: str




