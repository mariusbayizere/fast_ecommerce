from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import  Create_Student, Update_Student
from sqlmodel import select, desc
from .models import Student
from fastapi.exceptions import HTTPException



class studentservice:

    async def get_all_students(self, session: AsyncSession):
        """This is function is responsible for returning all student information

        Args:
            session (AsyncSession): 

        Returns:
            _type_: return all student data from server
        """
        statement = select(Student).order_by(Student.LastName.desc())
        result = await session.exec(statement)
        return result.all()

    async def get_student_by_id(self, student_id: int, session: AsyncSession):
        """ This function is responsible for returning a student information by id

        Args:
            student_id (int): receive student_id to searching student
            session (AsyncSession): will receive session as arguments 

        Returns:
            _type_: return student data if found else return None
        """
        statement = select(Student).where(Student.id == student_id)
        result = await session.exec(statement)
        student = result.first()
        return student if student is not None else None



    async def get_student_by_email(self, email: str, session: AsyncSession):
        """ This function is responsible for returning a student information by id

        Args:
            student_id (int): receive student_id to searching student
            session (AsyncSession): will receive session as arguments 

        Returns:
            _type_: return student data if found else return None
        """
        statement = select(Student).where(Student.Email == email)
        result = await session.exec(statement)
        student = result.first()
        return student if student is not None else None
    

    async def get_student_by_Phone_number(self, phone: str, session: AsyncSession):
        """ This function is responsible for returning a student information by id

        Args:
            student_id (int): receive student_id to searching student
            session (AsyncSession): will receive session as arguments 

        Returns:
            _type_: return student data if found else return None
        """
        statement = select(Student).where(Student.PhoneNumber == phone)
        result = await session.exec(statement)
        student = result.first()
        return student if student is not None else None


    async def create_student(self, student_data: Create_Student, session: AsyncSession):
        """This function is responsible for creating a new student
        and returning the student data.

        Args:
            student_data (Create_Student): will recieving student data as request body which having pydantic model to validate data
            session (AsyncSession): will receive session as arguments

        Returns:
            _type_: return student data
        """

        student_information =  student_data.model_dump()

        new_student = Student(
            **student_information
        )
        session.add(new_student)
        await session.commit()
        return new_student


    async def update_student(self, student_id: int, student_data_update: Update_Student, session:AsyncSession):
        """This function is responsible for updating a student information
        and returning the updated student data.

        Args:
            student_id (int): will receive student id to update
            student_data_update (Update_Student): will receive student data to update which is having pydantic model
            session (AsyncSession): will receive session as arguments

        Returns:
            _type_: return student data if found else return None
        """
        student_id = await self.get_student_by_id(student_id, session)
        if not student_id:
            return None
        student_information = student_data_update.model_dump()
        for key, value in student_information.items():
            setattr(student_id, key, value)
        session.commit()
        return student_id

    async def delete_student(self, student_id: int, session: AsyncSession):
        """This function is responsible for deleting a student
        and returning the student data.

        Args:
            student_id (int): will receive student id to delete
            session (AsyncSession): will receive session as arguments

        Returns:
            _type_: return student data if found else return None
        """
        student_delete = await self.get_student_by_id(student_id, session)
        if student_delete is not None:
            await session.delete(student_delete)
            await session.commit()
            return student_delete
        else:
            return None
