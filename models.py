from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any
from datetime import datetime
from bson import ObjectId

# Custom ObjectId type for Pydantic v2
class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler):
        from pydantic_core import core_schema
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ])
        ], serialization=core_schema.plain_serializer_function_ser_schema(str))

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

# Course Models
class Course(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    description: str
    age_group: str = Field(alias="ageGroup")
    duration: str
    projects: str
    icon: str
    color: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True

# Enrollment Models
class EnrollmentCreate(BaseModel):
    parent_name: str = Field(alias="parentName")
    child_name: str = Field(alias="childName")
    email: EmailStr
    phone: str
    child_age: int = Field(alias="childAge", ge=6, le=18)
    course: str
    message: Optional[str] = None

    class Config:
        populate_by_name = True

class Enrollment(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    parent_name: str
    child_name: str
    email: EmailStr
    phone: str
    child_age: int
    course: str
    message: Optional[str] = None
    status: str = "pending"  # pending, contacted, enrolled, cancelled
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True

# Game Models
class Game(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    image: str
    play_store_url: str = Field(alias="playStoreUrl")
    category: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True

# Testimonial Models
class Testimonial(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    role: str
    content: str
    rating: int = Field(ge=1, le=5)
    avatar: str
    is_approved: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True

# Schedule Models
class TimeSlot(BaseModel):
    time: str
    course: str
    level: str

class Schedule(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    day: str
    slots: List[TimeSlot]
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True
