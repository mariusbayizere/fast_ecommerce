from pydantic import BaseModel

class Student(BaseModel):
       id: int 
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