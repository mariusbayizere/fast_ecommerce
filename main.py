from fastapi import FastAPI, status
from typing import Optional
from pydantic import BaseModel
from typing import List
from fastapi.exceptions import HTTPException


app =FastAPI()


@app.get('/')
async def read_root():
    """
    This is the root function that returns a welcome message.
    """
    return {"Message":"Hello Marius"}



@app.get('/greet/{name}')
async def greeting(name: str, age : int)-> dict:
    """
    This is a greeting function that takes a name and age as parameters.
    It returns a dictionary with the name and age.
    """
    return {"Message":f"my name is {name} I have ", "Age" : age}


@app.get('/greets')
async def greeting_name(name: Optional[str]="User", age : Optional[int]=20)-> dict:
    """"
    This is a greeting function that takes a name and age as parameters.
    It returns a dictionary with the name and age.
    """
    return {"Message":f"My name is {name}", "Age":age}



Students = [
    {
        "id":1,
        "FirstName":"Bayizere",
        "LastName":"Marius",
        "Email":"bayizeremarius119@gmail",
        "PhoneNumber":"078888888",
        "Gender":"Male",
        "Nationality":"Rwandan"
    },
        {
        "id":2,
        "FirstName":"Abijuru",
        "LastName":"Raissa",
        "Email":"raissabijuru@gmail",
        "PhoneNumber":"078888882",
        "Gender":"Famale",
        "Nationality":"Rwandan"
    },
        {
        "id":3,
        "FirstName":"Iradukunda",
        "LastName":"Feza",
        "Email":"feza@gmail",
        "PhoneNumber":"078882888",
        "Gender":"Famile",
        "Nationality":"Rwandan"
    },
        {
        "id":4,
        "FirstName":"byiringiro",
        "LastName":"Danny",
        "Email":"byiringiro@gmail",
        "PhoneNumber":"078888868",
        "Gender":"Male",
        "Nationality":"Rwandan"
    }
    ,
        {
        "id":5,
        "FirstName":"Shema",
        "LastName":"Rogers",
        "Email":"shema@gmail",
        "PhoneNumber":"078888988",
        "Gender":"Male",
        "Nationality":"Rwandan"
    },
        {
        "id":6,
        "FirstName":"Manishimwe",
        "LastName":"Eric",
        "Email":"eric@gmail",
        "PhoneNumber":"078881888",
        "Gender":"Male",
        "Nationality":"Rwandan"
    },
        {
        "id":7,
        "FirstName":"Mugisha",
        "LastName":"Eric",
        "Email":"mugisha@gmail",
        "PhoneNumber":"078888880",
        "Gender":"Male",
        "Nationality":"Rwandan"
    }
]



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

@app.get('/students', response_model=List[Student])
async def get_students()-> list:
    """
    This function returns a list of students.
    """
    return Students


@app.post('/students', status_code=status.HTTP_201_CREATED)
async def create_student(student_data: Student) -> dict:
    """
    This function creates a new student and returns the student data.
    """
    new_student = student_data.model_dump()
    Students.append(new_student)
    return new_student


@app.get('/students/{Student_id}', status_code=status.HTTP_200_OK)
async def get_student(Student_id: int)-> dict:
    """
    This function returns a student with the given ID.
    """
    for student in Students:
          if student['id'] == Student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")
    

@app.put('/students/{student_id}', status_code=status.HTTP_200_OK)
async def Update_student(student_id:int, student_update: Update_Student)-> dict:
    """
    This function updates a student with the given ID and returns the updated student data.
    """
    for student in Students:
          if student['id'] == student_id:
               student['FirstName'] = student_update.FirstName
               student['LastName'] = student_update.LastName
               student['Email'] = student_update.Email
               student['PhoneNumber'] = student_update.PhoneNumber
               student['Gender'] = student_update.Gender
               student['Nationality'] = student_update.Nationality
               return student
    raise HTTPException(status_code=404, detail="Student not found")
            