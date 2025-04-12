from fastapi import APIRouter, status
from typing import List, Optional
from src.students.student_date import Students
from .schemas import Student, Update_Student
from fastapi.exceptions import HTTPException



student_router = APIRouter()


# @student_router.get('/')
# async def read_root():
#     """
#     This is the root function that returns a welcome message.
#     """
#     return {"Message":"Hello Marius"}



# @student_router.get('/greet/{name}')
# async def greeting(name: str, age : int)-> dict:
#     """
#     This is a greeting function that takes a name and age as parameters.
#     It returns a dictionary with the name and age.
#     """
#     return {"Message":f"my name is {name} I have ", "Age" : age}


# @student_router.get('/greets')
# async def greeting_name(name: Optional[str]="User", age : Optional[int]=20)-> dict:
#     """"
#     This is a greeting function that takes a name and age as parameters.
#     It returns a dictionary with the name and age.
#     """
#     return {"Message":f"My name is {name}", "Age":age}


@student_router.get('/', response_model=List[Student])
async def get_students()-> list:
    """
    This function returns a list of students.
    """
    return Students


@student_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_student(student_data: Student) -> dict:
    """
    This function creates a new student and returns the student data.
    """
    new_student = student_data.model_dump()
    Students.append(new_student)
    return new_student


@student_router.get('/{Student_id}', status_code=status.HTTP_200_OK)
async def get_student(Student_id: int)-> dict:
    """
    This function returns a student with the given ID.
    """
    for student in Students:
          if student['id'] == Student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")
    

@student_router.put('/{student_id}', status_code=status.HTTP_200_OK)
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
            

@student_router.delete('/{student_id}', status_code= status.HTTP_200_OK)
async def delete_student(student_id:int)-> dict:
    """
    This function deletes a student with the given ID and returns a success message.
    """
    for student in Students:
          if student['id'] == student_id:
               Students.remove(student)
               return {"Message":"Student deleted successfully"}
    raise HTTPException(status_code=404, detail="Student not found")