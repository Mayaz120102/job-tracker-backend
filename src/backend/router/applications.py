from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from typing import Optional
from backend.database import db_dependency
from backend.models import Applications, ApplicationStatus
from backend.router.auth import get_current_user
from backend.schemas import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from sqlalchemy import or_

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


# get all applications


@router.get("/applications", response_model=list[ApplicationResponse])
def get_all_applications(
    user: user_dependency,
    db: db_dependency,
    status: Optional[ApplicationStatus] = Query(default=None),
    search: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):

    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized User")

    query = db.query(Applications).filter(Applications.owner_id == user.get("id"))

    if status is not None:
        query = query.filter(Applications.status == status)

    if search is not None:
        query = query.filter(
            or_(
                Applications.company_name.ilike(f"%{search}%"),
                Applications.job_title.ilike(f"%{search}%"),
            )
        )

    return query.offset(skip).limit(limit).all()


# speicifc application
@router.get("/applications/{application_id}", response_model=ApplicationResponse)
def get_specific_application(
    user: user_dependency, db: db_dependency, application_id: int
):

    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized User")

    specific_appication = (
        db.query(Applications)
        .filter(Applications.owner_id == user.get("id"))
        .filter(Applications.id == application_id)
        .first()
    )
    if specific_appication is not None:
        return specific_appication
    else:
        raise HTTPException(status_code=404, detail="application is not found")


# create application
@router.post(
    "/applications",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    user: user_dependency, db: db_dependency, new_application: ApplicationCreate
):

    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized User")

    application_model = Applications(
        **new_application.model_dump(), owner_id=user.get("id")
    )
    db.add(application_model)
    db.commit()
    db.refresh(application_model)

    return application_model


# update application
@router.put(
    "/applications/{application_id}",
    response_model=ApplicationResponse,
    status_code=status.HTTP_200_OK,
)
def update_application(
    user: user_dependency,
    db: db_dependency,
    application_id: int,
    update_application: ApplicationUpdate,
):

    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized User")

    application = (
        db.query(Applications)
        .filter(Applications.owner_id == user.get("id"))
        .filter(Applications.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(status_code=404, detail="Application is not Found")

    update_data = update_application.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(application, key, value)

    db.commit()
    db.refresh(application)

    return application


@router.delete("/applications/{application_id}")
def delete_application(user: user_dependency, db: db_dependency, application_id: int):

    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized User")

    application = (
        db.query(Applications)
        .filter(Applications.owner_id == user.get("id"))
        .filter(Applications.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(status_code=404, detail="Application is not Found")

    db.query(Applications).filter(Applications.owner_id == user.get("id")).filter(
        Applications.id == application_id
    ).delete()

    db.commit()

    return JSONResponse(
        status_code=200, content={"message": "Application Deleted succesfully"}
    )
