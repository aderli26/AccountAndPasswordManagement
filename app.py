from flask import request, Flask,abort,make_response
from utils import connect_DB,http_response
import json 
import re
import time
import bcrypt
import settings
import sqlite3
def get_hashed_password(plain_text_password):

    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):

    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)

app = Flask(__name__)


@app.route('/register', methods=['POST'])
def user_register():
    body = json.loads(request.data)
    username = body.get('username')
    password = body.get('password')
    if (username is not None) and (password is not None) :
        #check string matches
        if 3 > len(username):
            return http_response(success=False,reason='Username is too short')
        elif 32 < len(username):
            return http_response(success=False,reason='Username is too long')
        if 3 > len(password):
            return http_response(success=False,reason='Password is too short')
        elif 32 < len(password):
            return http_response(success=False,reason='Password is too long')
        
        elif re.search('[a-z]', password) and re.search('[A-Z]', password) and re.search('[0-9]', password):
            pass
        else:
            return http_response(success=False,reason='Password must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number')
        
        # find account
        con=connect_DB(settings.SQLITE_DB_PATH)
        query="SELECT username FROM users WHERE username =?"
        try:
            cursor=con.execute(query,(username,))
            account = cursor.fetchone()
            con.commit()
        except sqlite3.Error as e:
            con.close()
            return http_response(success=False,reason=str(e)),500
        
        if account:
            con.close()
            return http_response(success=False,reason='Username already exists')
        else:
            try:
                query="INSERT INTO users (`username`,`password`) VALUES (?, ?)"
                cursor.execute(query,(username,get_hashed_password(password)))
                con.commit()
            except sqlite3.Error as e:
                con.close()
                return http_response(success=False,reason=str(e)),500
            con.close()
            return http_response(success=True,reason='Successfully registered')
    else:
        return http_response(success=True,reason='Missing username or password')


@app.route('/login', methods=['POST'])
def user_login():
    body = json.loads(request.data)
    username = body.get('username')
    password = body.get('password')
    if (username is not None) and (password is not None) :
        # find account
        con=connect_DB(settings.SQLITE_DB_PATH)
        query="SELECT `username`,`password` FROM users WHERE username =?"
        try:
            cursor=con.execute(query,(username,))
            con.commit()
            account = cursor.fetchone()
        except sqlite3.Error as e:
            con.close()
            return http_response(success=False,reason=str(e)),500
        
        if account:
            account_password=account[1]
            # check password
            if not check_password(password,account_password):
                try:
                    query="SELECT `retry`,`timestamp` FROM login_retry WHERE username =?"
                    cursor=con.execute(query,(username,))
                    con.commit()
                    retry= cursor.fetchone()
                except sqlite3.Error as e:
                    con.close()
                    return http_response(success=False,reason=str(e)),500
                if retry:
                    # if failed, check retry times
                    TIMEOUT_SEC=60
                    MAX_RETRY=5
                    retry_time=retry[0]
                    last_time=retry[1]


                    if retry_time>=MAX_RETRY and (time.time()-last_time)<=TIMEOUT_SEC:
                        con.close()
                        return http_response(success=False,reason="Please wait for one minute"),403
                    else:
                        if (time.time()-last_time)>=TIMEOUT_SEC:
                            # if timeout reset retry time
                            retry_time=1
                        else:
                            # increase retry time
                            retry_time+=1
                            
                        query="UPDATE login_retry SET `retry`=? , `timestamp`=?"
                        try:
                            cursor=con.execute(query,(retry_time,time.time()))
                            con.commit()
                            con.close()
                        except sqlite3.Error as e:
                            con.close()
                            return http_response(success=False,reason=str(e)),500
                else:
                    query="INSERT INTO login_retry (`username`,`retry`,`timestamp`) VALUES (?,?, ?)"
                    try:
                        cursor=con.execute(query,(username,1,time.time()))
                        con.commit()
                        con.close()
                    except sqlite3.Error as e:
                        con.close()
                        return http_response(success=False,reason=str(e)),500
                    
                return http_response(success=False,reason='Wrong password')
            else:
                con.close()
                return http_response(success=True,reason='Successfully verified')
        else:
            con.close()
            return http_response(success=False,reason='Username not found')

if __name__=="__main__":
    app.run()

