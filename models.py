from typing import Optional, List
from pydantic import validator
from sqlalchemy import Column
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


def to_camel(name):
    return "".join(
        x.capitalize() if i > 0 else x for i, x in enumerate(name.split("_"))
    )


class Products(SQLModel, table=True):
    product_id: str = Field(default=None, primary_key=True, alias='_id')
    name: str
    unit_of_measure: str
    quantity_for_one_foodstuff: int
    created_at: datetime
    updated_at: datetime
    created_by: str
    category: str
    cupboard: str
    updated_by: str
    current_stock: int

    @validator("product_id", "created_by", "category", "cupboard", "updated_by", pre=True)
    def unnest_id(cls, v):
        return v["$oid"]

    @validator("created_at", "updated_at", pre=True)
    def unnest_date(cls, v):
        return v["$date"]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

class FamilyMembers(SQLModel, table=True):

    __tablename__: str = "family_members"

    family_member_id: str = Field(default=None, primary_key=True, alias='_id')

    families: List["Families"] = Relationship(back_populates="family_members")

    @validator("family_member_id", pre=True)
    def unnest_id(cls, v):
        return v["$oid"]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

class Families(SQLModel, table=True):
    family_id: str = Field(default=None, primary_key=True, alias='_id')
    family_members_id: List[str] = Field(default=None, foreign_key="family_members.family_member_id", alias='familyMembers')
    family_members: FamilyMembers = Relationship(back_populates="families")

    @validator("family_id", pre=True)
    def unnest_id(cls, v):
        return v["$oid"]

    @validator("family_members_id", pre=True)
    def unnest_family_members(cls, v):
        return [fm["$oid"] for fm in v]


    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True



# class Families(SQLModel, table=True):
#     family_id: str = Field(default=None, primary_key=True, alias='_id')
#     name: str
#     city: str
#     housing_details: Optional[str]
#     created_at: datetime
#     updated_at: datetime
#     additional_info: Optional[str]
#     last_visit_at: Optional[datetime]
#     know_association_by: Optional[str]
#     certificate_of_residence_provided_at: Optional[str] # To Do: cast to date

#     @validator("family_id", pre=True)
#     def unnest_id(cls, v):
#         return v["$oid"]

#     @validator("created_at", "updated_at", "last_visit_at", pre=True)
#     def unnest_date(cls, v):
#         return v["$date"]


#     class Config:
#         alias_generator = to_camel
#         allow_population_by_field_name = True

# class FamilyMembers(SQLModel, table=True):

#     __tablename__: str = "family_members"

#     family_member_id: str = Field(default=None, primary_key=True, alias='_id')
#     gender: str
#     adult_or_child: Optional[str]
#     surname: Optional[str]
#     birth_date: Optional[datetime] = Field(alias='birthday')
#     created_at: Optional[datetime]
#     updated_at: Optional[datetime]

#     @validator("family_member_id", pre=True)
#     def unnest_id(cls, v):
#         return v["$oid"]

#     @validator("created_at", "updated_at", "birth_date", pre=True)
#     def unnest_date(cls, v):
#         return v["$date"]

#     class Config:
#         alias_generator = to_camel
#         allow_population_by_field_name = True

class VisitEvents(SQLModel, table=True):

    __tablename__: str = "visit_events"

    visit_id: str = Field(default=None, primary_key=True, alias='_id')
    family_id: str = Field(alias='family')
    created_at: datetime
    updated_at: datetime

    @validator("visit_id", "family_id", pre=True)
    def unnest_id(cls, v):
        return v["$oid"]

    @validator("created_at", "updated_at", pre=True)
    def unnest_date(cls, v):
        return v["$date"]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

# class Categories
