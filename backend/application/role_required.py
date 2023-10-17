from functools import wraps
from flask_jwt_extended import get_jwt_identity
from application.models import * 
from application.database import db

def role_required(roles):

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                print("rr 1")
                current_user = get_jwt_identity()
                id = current_user.get('id')

                if not id:
                    print("rr 2")
                    return {'message':'Invalid Token'} , 410
                
                user = db.session.query(User).filter(User.id==id).first()
                if not user:
                    print("rr 3")
                    return {'message':'Not valid User'} , 411

                if roles==['Admin']:
                    print("rr 4")
                    u_role  = db.session.query(RolesUsers).filter(RolesUsers.user_id==id).first()
                    if u_role.role_id==1:
                        print("rr 5")
                        return fn(*args, **kwargs)
                    else:
                        print("rr 6")
                        return {'message':'Unauthorised'} , 412

                elif roles ==['User']:
                    print("rr 7")
                    u_role  = db.session.query(RolesUsers).filter(RolesUsers.user_id==id).first()
                    if u_role.role_id==2:
                        print("rr 8")
                        return fn(*args, **kwargs)
                    else:
                        print("rr 9")
                        return {'message':'Unauthorised'} , 412

                # print('4')
                # print(type(id))
                # u_role  = db.session.query(RolesUsers).filter(RolesUsers.user_id==user.id).first()
                # print(u_role)
                # urole = db.session.query(Role).filter(Role.id==u_role.role_id).first()
                # print('6')
                # if not urole.name in roles:
                #     print('00')
                #     return {'message':'Unauthorised'} , 412
                # return fn(*args, **kwargs)

            except Exception as e:
                return {'message':'Internal Server Error. Error at role_required'} , 413 
        return wrapper
    return decorator