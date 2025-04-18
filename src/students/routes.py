from fastapi import APIRouter, status, Depends
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import det_session
from src.students.models import Student
from src.students.services import studentservice
from .schemas import StudentResponse, Update_Student, Create_Student
from fastapi.exceptions import HTTPException
from src.auth.dependencies import Access_token_Bearer



student_router = APIRouter()
student_service = studentservice()
access_tokens_bearer = Access_token_Bearer()


@student_router.get('/', response_model=List[StudentResponse])
async def get_students(session: AsyncSession=Depends(det_session), user_details=Depends(access_tokens_bearer))-> List[StudentResponse]:
    """This function is responsible for returning all student information

    Args:
        session (AsyncSession): _description_. Defaults to Depends(det_session).

    Returns:
        list: return all student data from server
    """
    students = await student_service.get_all_students(session)

    return students


@student_router.post('/', status_code=status.HTTP_201_CREATED, response_model=StudentResponse)
async def create_student(student_data: Create_Student, session: AsyncSession= Depends(det_session)) -> dict:
    """This function is responsible for creating a new student
    and returning the student data.

    Args:
        student_data (Student): will recieving student data as request body which having pydantic model to validate data
        session (AsyncSession, optional): . Defaults to Depends(det_session).

    Returns:
        dict: return student data
    """
    new_student = await student_service.create_student(student_data, session)
    return new_student


@student_router.get('/{Student_id}', response_model= StudentResponse, status_code=status.HTTP_200_OK)
async def get_student(Student_id: int, session:AsyncSession= Depends(det_session))-> StudentResponse:
        """This function is responsible for returning a student information by id

        Args:
            Student_id (int): receive student_id to searching student
            session (AsyncSession, optional): _description_. Defaults to Depends(det_session).

        Raises:
            HTTPException: if student not found

        Returns:
            dict: return student data if found else return None
        """

        student_by_id = await student_service.get_student_by_id(Student_id, session)

        if student_by_id is None:
             raise HTTPException(status_code=404, detail=f"Student with ID : {Student_id} is not found")

        return student_by_id
    
    

@student_router.put('/{student_id}', response_model=StudentResponse, status_code=status.HTTP_200_OK)
async def Update_student(student_id: int, student_update: Update_Student, session: AsyncSession = Depends(det_session))-> dict:
    """This function is responsible for updating a student information
    and returning the updated student data.

    Args:
        student_id (int): will receive student id to update
        student_update (Update_Student): will receive student data to update which is having pydantic model
        session (AsyncSession): will receive session as arguments

    Raises:
        HTTPException: if student not found

    Returns:
        dict: return student data
    """
    
    update_student_result = await student_service.update_student(student_id, student_update, session)

    if update_student_result:
        return update_student_result
    else:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} is not found")
            

@student_router.delete('/{student_id}', status_code= status.HTTP_200_OK)
async def delete_student(student_id:int, session: AsyncSession=Depends(det_session))-> dict:
    """This function is responsible for deleting a student
    and returning the student data.

    Args:
        student_id (int): will receive student id to delete
        session (AsyncSession, optional): _description_. Defaults to Depends(det_session).

    Raises:
        HTTPException: if student not found

    Returns:
        dict: return student data
    """
    student_delete = await student_service.delete_student(student_id, session)

    if student_delete:
        return {"message": f"Student with ID {student_id} is deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} is not found")