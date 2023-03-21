import hashlib

from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.app.logger import log
from app.models.db import users as db_users, companies as db_companies
from app.app import companies as app_companies


def get_user_by_username(db: Session, username: str):
    return db.query(db_users.User).filter(db_users.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(db_users.User).filter(db_users.User.email == email).first()


def get_user_by_id(db: Session, user_id: int, access_level=None, from_user_id=None):
    log.input(db, user_id, access_level, from_user_id)
    if (not access_level and not from_user_id) or access_level == 1:
        return db.query(db_users.User).filter(db_users.User.id == user_id).first()
    else:
        if access_level == 2:
            companies_id = db.query(db_users.UserCompany.company_id).join(db_companies.Company).filter(db_users.UserCompany.user_id == from_user_id).filter(db_companies.Company.inactive != True).all()
            for company_id in companies_id:
                user = db.query(db_users.User).join(db_users.UserCompany).join(db_companies.Company).filter(db_users.UserCompany.company_id == company_id[0]).filter(db_users.UserCompany.user_id == user_id).filter(db_companies.Company.inactive != True).first()
                if user:
                    return user
                else:
                    query = db.query(db_users.User)
                    user_ids = [i[0] for i in db.query(db_users.UserCompany.user_id).all()]
                    user = query.filter(db_users.User.id.notin_(user_ids)).filter(db_users.User.id == user_id).first()
                    if user:
                        return user

            raise HTTPException(status_code=406, detail="User not in yours company!")
        else:
            raise HTTPException(status_code=403, detail="You don't have permissions")


def add_user_company(company_id, user_id, db):
    log.input(company_id, user_id, db)
    data = db.query(db_users.UserCompany).filter(db_users.UserCompany.company_id == company_id).filter(db_users.UserCompany.user_id == user_id).first()
    if data:
        raise HTTPException(status_code=406, detail="User already in group")
    user_company = db_users.UserCompany(user_id=user_id, company_id=company_id)
    db.add(user_company)
    db.commit()
    return {'status': '+ company'}


def remove_user_company(company_id, user_id, db):
    log.input(company_id, user_id, db)
    obj = db.query(db_users.UserCompany).filter(db_users.UserCompany.company_id == company_id).filter(db_users.UserCompany.user_id == user_id).delete()
    db.commit()
    if obj:
        return {'status': '- company'}
    else:
        return {'status': 'failed'}


def get_current_user(db, auth: AuthJWT):
    log.input(db, auth)
    auth.jwt_required()
    current_user = get_user_by_id(db, auth.get_jwt_subject())
    return current_user


def check_access(db, auth: AuthJWT, needed):
    log.input(db, auth, needed)
    access_level = get_access_level(db, auth.get_jwt_subject())
    if access_level > needed:
        raise HTTPException(status_code=406, detail="You don't have permissions")


def get_access_level(db, user_id):
    log.input(db, user_id)
    role = db.query(db_users.User.role).filter(db_users.User.id == user_id).first()
    if not role:
        raise HTTPException(status_code=406, detail="User does't exists")
    role = role[0]
    return 1 if role == 'root' else 2 if role == 'admin' else 3


def get_count_active_root_users(db):
    users = db.query(db_users.User).filter(db_users.User.role == 'root').filter(db_users.User.inactive != True).all()
    return len(users)


def update_user(update_data, db: Session, auth):
    log.input(update_data, db, auth)
    user = db.query(db_users.User).filter(db_users.User.id == update_data.id).first()
    admin_user = get_current_user(db, auth)
    if admin_user.role == 'root':
        check_access(db, auth, 1)
    elif update_data.email or (update_data.role and update_data.role != 'root') or (update_data.password and auth.get_jwt_subject() != update_data.id):
        check_access(db, auth, 2)
        if update_data.role != 'admin' and update_data.id == user.id and update_data.role:
            raise HTTPException(status_code=406, detail="You don't have permissions")
        # if get_access_level(db, update_data.id) < 3:
        #     HTTPException(status_code=405, detail="You don't have permissions")
    else:
        if update_data.id != auth.get_jwt_subject() and get_current_user(db, auth).role == 'manager':
            HTTPException(status_code=405, detail="You can't manage password to other user")
        else:
            HTTPException(status_code=405, detail="You don't have permissions")

    root_access = get_access_level(db, auth.get_jwt_subject())
    to_access = get_access_level(db, user.id)
    if root_access >= to_access and auth.get_jwt_subject() != user.id and root_access != 1:
        raise HTTPException(status_code=406, detail="You don't have permissions")
    if auth.get_jwt_subject() == user.id:
        if str(update_data.inactive).lower() == 'true':
            raise HTTPException(status_code=406, detail="You can't set inactive to yourself")

    if update_data.username:
        if not get_user_by_username(db, update_data.username):
            user.username = update_data.username
        elif user.username != update_data.username:
            raise HTTPException(status_code=409, detail="User already exists")

    if update_data.email:
        if not get_user_by_email(db, update_data.email):
            user.email = update_data.email
        elif user.email != update_data.email:
            raise HTTPException(status_code=409, detail="Email already exists")

    if update_data.role:
        user.role = update_data.role
    if update_data.password:
        user.hash_password = hashlib.md5(update_data.password.encode('utf-8')).hexdigest()
    # if update_data.first_name:
    user.first_name = update_data.first_name
    # if update_data.last_name:
    user.last_name = update_data.last_name

    if update_data.inactive:
        if update_data.inactive.lower() == 'true':
            user.inactive = True
        else:
            user.inactive = False

    db.commit()
    db.refresh(user)
    log.output(user)
    return user


def check_user_in_companies(db, user_id, input_companies):
    log.input(db, user_id, input_companies)
    if input_companies:
        companies: list = db.query(db_users.UserCompany.company_id).join(db_companies.Company).filter(db_users.UserCompany.user_id == user_id).filter(db_companies.Company.inactive != True).all()
        for i in input_companies:
            if i not in [company[0] for company in companies]:
                raise HTTPException(status_code=403, detail="You don't have permissions to watch this company")
    else:
        raise HTTPException(status_code=403, detail="Select companies")


def set_inactive_user(db: Session, user_id):
    log.input(db, user_id)
    user = db.query(db_users.User).filter(db_users.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="User does not exist")
    user.inactive = True
    db.commit()
    db.refresh(user)
    return user


def create_user(db: Session, user):
    log.input(db, user)
    hashed_password = hashlib.md5(user.password.encode('utf-8')).hexdigest()
    db_user = db_users.User(email=user.email,
                            hash_password=hashed_password,
                            role='manager',
                            inactive=False,
                            username=user.username,
                            last_name=user.last_name,
                            first_name=user.first_name,
                            description=user.description)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_company_users(db, company_id, access_level, from_user_id):
    log.input(db, company_id, access_level, from_user_id)
    if access_level == 1:
        return db.query(db_users.User).join(db_users.UserCompany).filter(db_users.UserCompany.company_id == company_id).all()
    elif access_level == 2:
        if db.query(db_users.User).join(db_users.UserCompany).join(db_companies.Company).filter(and_(db_users.UserCompany.company_id == company_id, db_users.UserCompany.user_id == from_user_id)).first():
            return db.query(db_users.User).join(db_users.UserCompany).join(db_companies.Company).filter(db_users.UserCompany.company_id == company_id).all()
        else:
            return []
    else:
        return []


def get_all_users(db, access_level, user_id, role, company_ids, inactive):
    log.input(db, access_level, user_id)
    if access_level == 1:
        query = db.query(db_users.User)

        if role != 'all':
            query = query.filter(db_users.User.role == role)
        if company_ids != [0]:

            if company_ids == [-1]:
                company_ids = []
            if not company_ids:
                user_ids = [i[0] for i in db.query(db_users.UserCompany.user_id).all()]
                query = query.filter(db_users.User.id.notin_(user_ids)).filter(db_users.User.role != 'root')
            else:
                query = query.join(db_users.UserCompany).filter(db_users.UserCompany.company_id.in_(company_ids))

        if inactive:
            query = query.filter(db_users.User.inactive == True)

        return query.all()

    elif access_level == 2:
        companies_id = db.query(db_users.UserCompany.company_id).join(db_companies.Company).filter(db_users.UserCompany.user_id == user_id).filter(db_companies.Company.inactive != True).all()
        users = []

        for company_id in companies_id:
            company_id = company_id[0]
            query = db.query(db_users.User).join(db_users.UserCompany).join(db_companies.Company).filter(db_users.UserCompany.company_id == company_id)
            if role != 'all':
                query = query.filter(db_users.User.role == role)

            if company_ids != [0]:
                if company_ids and companies_id != [-1]:
                    query = query.filter(db_users.UserCompany.company_id.in_(company_ids))

            if inactive:
                query = query.filter(db_users.User.inactive == True)
            else:
                query = query.filter(db_companies.Company.inactive != True)

            users.extend(query.filter(db_users.User.role != 'root').all())

        query = db.query(db_users.User)

        if company_ids != [0]:
            if company_ids == [-1]:
                user_ids = [i[0] for i in db.query(db_users.UserCompany.user_id).all()]

                query = query.filter(db_users.User.id.notin_(user_ids))

        users.extend(query.filter(db_users.User.role != 'root').all())

        for user in users:
            while users.count(user) > 1:
                users.remove(user)
        return users
    else:
        return []


def update_user_companies(db, companies_id, user_id, access_level, from_user_id):
    log.input(db, companies_id, user_id, access_level, from_user_id)
    if access_level == 2:
        companies = app_companies.get_user_companies(from_user_id, db)
        suc = False
        for i in companies_id:
            if i in companies:
                suc = True
                break
        if not (suc or companies == companies_id):
            raise HTTPException(status_code=406, detail="You don't have permissions")
    elif access_level == 3:
        raise HTTPException(status_code=406, detail="You don't have permissions")

    db.query(db_users.UserCompany).filter(db_users.UserCompany.user_id == user_id).delete()
    db.commit()

    response = []

    for i in companies_id:
        obj = db_users.UserCompany(user_id=user_id, company_id=i)
        response.append(obj)
        db.add(obj)

    db.commit()

    return {'updated_companies': response}


def new_user_with_companies(user, db, auth, access_level):
    if access_level < 3:
        new_user = create_user(db, user)
        update_user_companies(db, user.companies_id, new_user.id, access_level, auth.get_jwt_subject())
    else:
        raise HTTPException(status_code=406, detail="You don't have permissions")

