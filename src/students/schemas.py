from pydantic import BaseModel

class StudentResponse(BaseModel):
       id: int 
       FirstName: str
       LastName: str
       Email: str
       PhoneNumber: str 
       Gender: str
       Nationality: str


class Create_Student(BaseModel): 
       FirstName: str
       LastName: str
       Email: str
       PhoneNumber: str 
       Gender: str
       Nationality: str

class Update_Student(BaseModel): 
       FirstName: str
       LastName: str
       Email: str
       PhoneNumber: str 
       Gender: str
       Nationality: str