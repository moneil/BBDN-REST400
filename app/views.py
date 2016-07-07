from flask import render_template
from flask import request
from app import app
import json
from app import auth
from app import learn_version
from app import courses
from app import users
from app import memberships

from pylti.flask import lti

@app.route('/is_up', methods=['GET'])
def isUp():

    return render_template('up.html')

@app.route('/')
@app.route('/index')
def index():
    """ 
    Return the demo index page
    """
    return app.send_static_file('index.html')

@app.route('/config')
def config():
    """
    Return config page
    """
    #user = {'nickname': 'Mark'}  # fake user
    settings = {'settings':app.config}
    return render_template('config.html',
                           settings=settings)

@app.route('/authz')
@app.route('/authorize')
def authorize():
    """
    Return OAuth Token
    """
    settings = {'settings':app.config}
    target = app.config["TARGET_URL"]
    auth_session = auth.AuthToken(target,
                                  app.config["CERT_PATH"])
    token = auth_session.getToken(target, 
                                  app.config["OAUTH_KEY"], 
                                  app.config["OAUTH_SECRET"])
    app.config["TOKEN"]=token

    expires_in = auth_session.getExpiresIn()

    return render_template('auth.html',
                           target_url=target,
                           oauth_token=token,
                           expires_in=expires_in,
                           config_token=app.config["TOKEN"],
                           settings=settings)

@app.route('/learn_version')
def lrnVersion():
    """
    Return Learn Version
    """
    settings = {'settings':app.config}
    #lrnSsn = 
    target = app.config["TARGET_URL"]
    #version is a JSON.parsed
    
    result = learn_version.LearnVersion().getLearnVersion(target, app.config["OAUTH_KEY"], app.config["OAUTH_SECRET"], app.config['TOKEN'])
    versionJSON = json.dumps(result)
    return render_template('learn_version.html',
                           target_url=app.config["TARGET_URL"],
                           version=versionJSON,
                           result=result["learn"],
                           settings=settings)

@app.route('/courses')
@app.route('/courses/<paginateId>')
def Courses(paginateId=None):
    """
    Return Course Collection
    """
    settings = {'settings':app.config}
    target = app.config["TARGET_URL"] + app.config["COURSES_PATH"]
    if paginateId is None:
        # This is only used by the visit_form on the index page.
        print("paginateId = None: Using configured courses_path.")
    else:
        print("paginateId = %s" % paginateId)
        target = (target[:(target.rfind('=')-len(target))])+"="+paginateId

    #check authZ
    if (app.config["TOKEN"] == ""):
        print("TOKEN NOT SET")
        authtarget = app.config["TARGET_URL"]

        auth_session = auth.AuthToken(authtarget,
                                      app.config["CERT_PATH"])
        token = auth_session.getToken(authtarget, 
                                      app.config["OAUTH_KEY"], 
                                      app.config["OAUTH_SECRET"])
        app.config["TOKEN"]=token
    
    result = courses.Courses().getCourses(target, app.config["OAUTH_KEY"], app.config["OAUTH_SECRET"], app.config['TOKEN'])
    coursesJSON = json.dumps(result)
    nextpageURL = result["paging"]["nextPage"]
    print("nextpageURL: %s" %nextpageURL)

    #app.config["COURSES_PATH"] = nextpageURL
    
    dataOffset = nextpageURL[(nextpageURL.rfind('=')+1-len(nextpageURL)):]
    
    print("dataOffset: %s" %dataOffset)
    print("dataOffset LIMIT: %s" % app.config["LIMIT"])

    limitInt = int(app.config["LIMIT"])
    dataOffsetInt = int(dataOffset)

    if (dataOffsetInt < limitInt):
        dataOffset = None

    print("dataOffset: %s" %dataOffset)

    return render_template('courses.html',
                           target_url=target,
                           coursesJSON=coursesJSON,
                           resultsJSON=result,
                           pagingJSON=result["paging"],
                           nextpageURL=nextpageURL,
                           dataOffset=dataOffset,
                           settings=settings)

@app.route('/users')
@app.route('/users/<paginateId>')
def Users(paginateId=None):
    """
    Return Users Collection
    """
    settings = {'settings':app.config}
    target = app.config["TARGET_URL"] + app.config["USERS_PATH"]
    if paginateId is None:
        # This is only used by the visit_form on the index page.
        print("paginateId = None: Using configured users_path.")
    else:
        print("paginateId = %s" % paginateId)
        target = (target[:(target.rfind('=')-len(target))])+"="+paginateId

    #check authZ
    if (app.config["TOKEN"] == ""):
        print("TOKEN NOT SET")
        authtarget = app.config["TARGET_URL"]

        auth_session = auth.AuthToken(authtarget,
                                      app.config["CERT_PATH"])
        token = auth_session.getToken(authtarget, 
                                      app.config["OAUTH_KEY"], 
                                      app.config["OAUTH_SECRET"])
        app.config["TOKEN"]=token
    
    result = courses.Courses().getCourses(target, app.config["OAUTH_KEY"], app.config["OAUTH_SECRET"], app.config['TOKEN'])
    usersJSON = json.dumps(result)
    nextpageURL = result["paging"]["nextPage"]
    print("nextpageURL: %s" %nextpageURL)

    #app.config["COURSES_PATH"] = nextpageURL
    
    dataOffset = nextpageURL[(nextpageURL.rfind('=')+1-len(nextpageURL)):]
    
    print("dataOffset: %s" %dataOffset)
    print("dataOffset LIMIT: %s" % app.config["LIMIT"])

    limitInt = int(app.config["LIMIT"])
    dataOffsetInt = int(dataOffset)

    if (dataOffsetInt < limitInt):
        dataOffset = None

    print("dataOffset: %s" %dataOffset)

    return render_template('users.html',
                           target_url=target,
                           usersJSON=usersJSON,
                           resultsJSON=result,
                           pagingJSON=result["paging"],
                           nextpageURL=nextpageURL,
                           dataOffset=dataOffset,
                           settings=settings)

@app.route('/courses/memberships/<courseId>')
def Memberships(courseId=None):
    """
    Return Course Memberships Collection
    """
    paginateId = request.args.get('paginateId', None)

    print("[views:Memberships] COURSE_ID: %s" % courseId)
    print("[views:Memberships] paginateId: %s" % paginateId)
    
    settings = {'settings':app.config}
    target = app.config["TARGET_URL"] + app.config["COURSE_MEMBERSHIPS_PATH"]
    #insert courseID into target

    target = target.replace("<courseId>", courseId)

    if paginateId is None:
        # This is only used by the visit_form on the index page.
        print("[views:Memberships] paginateId = None: Using configured users_path.")
    else:
        print("[views:Memberships] paginateId = %s" % paginateId)
        target = (target[:(target.rfind('=')-len(target))])+"="+paginateId

    print ("[views:Memberships] Altered target: %s" % target)

    #check authZ
    if (app.config["TOKEN"] == ""):
        print("[views:Memberships] TOKEN NOT SET")
        authtarget = app.config["TARGET_URL"]
        auth_session = auth.AuthToken(authtarget,
                                      app.config["CERT_PATH"])
        token = auth_session.getToken(authtarget, 
                                      app.config["OAUTH_KEY"], 
                                      app.config["OAUTH_SECRET"])
        app.config["TOKEN"]=token
    result = memberships.Memberships().getCourseMemberships(target, app.config["OAUTH_KEY"], app.config["OAUTH_SECRET"], app.config['TOKEN'])
    membersJSON = json.dumps(result)
    nextpageURL = None
    dataOffset = 0
    pagingJSON = None
    if ('paging' in result):
        if ('nextPage' in result['paging']):
            nextpageURL = result['paging']['nextPage']
            pagingJSON = result['paging']
            dataOffset = nextpageURL[(nextpageURL.rfind('=')+1-len(nextpageURL)):]

    print("[views:Memberships] nextpageURL: %s" % nextpageURL)    
    print("[views:Memberships] dataOffset: %s" %dataOffset)
    print("[views:Memberships] dataOffset LIMIT: %s" % app.config["LIMIT"])

    limitInt = int(app.config["LIMIT"])
    dataOffsetInt = int(dataOffset)
    if (dataOffsetInt < limitInt):
        dataOffset = None

    print("[views:Memberships] dataOffset: %s" %dataOffset)

    return render_template('coursememberships.html',
                            target_url=target,
                            membersJSON=membersJSON,
                            resultsJSON=result,
                            pagingJSON=pagingJSON,
                            nextpageURL=nextpageURL,
                            dataOffset=dataOffset,
                            selfCourseId=courseId,
                            settings=settings) 

@app.route('/course/<courseId>')
def Course(courseId=None):
    """
    Return Single Course identified by courseId
    """
    settings = {'settings':app.config}
    target = app.config["TARGET_URL"] + app.config["COURSE_PATH"]
    if (courseId is None):
        # This is only used by the visit_form on the index page.
        print("[view::Course] courseId = None: courseId required.")
    else:
        print("[view::Course] courseId = %s" % courseId)
        target += courseId
        print("[view::Course] target = %s" % target)

    #check authZ
    if (app.config["TOKEN"] == ""):
        print("TOKEN NOT SET")
        authtarget = app.config["TARGET_URL"]

        auth_session = auth.AuthToken(authtarget,
                                      app.config["CERT_PATH"])
        token = auth_session.getToken(authtarget, 
                                      app.config["OAUTH_KEY"], 
                                      app.config["OAUTH_SECRET"])
        app.config["TOKEN"]=token


  
    result = courses.Courses().getCourse(target, app.config["OAUTH_KEY"], app.config["OAUTH_SECRET"], app.config['TOKEN'])
    courseJSON = json.dumps(result)
    
    return render_template('course.html',
                           target_url=target,
                           courseJSON=courseJSON,
                           resultsJSON=result,
                           settings=settings)

@app.route('/user/<userId>')
def User(userId=None):
    """
    Return Single Course identified by courseId
    """
    settings = {'settings':app.config}
    target = app.config["TARGET_URL"] + app.config["USER_PATH"]
    if (userId is None):
        # This is only used by the visit_form on the index page.
        print("[view::User] userId = None: userId required.")
    else:
        print("[view::User] userId = %s" % userId)
        target += userId
        print("[view::User] target = %s" % target)

    #check authZ
    if (app.config["TOKEN"] == ""):
        print("TOKEN NOT SET")
        authtarget = app.config["TARGET_URL"]

        auth_session = auth.AuthToken(authtarget,
                                      app.config["CERT_PATH"])
        token = auth_session.getToken(authtarget, 
                                      app.config["OAUTH_KEY"], 
                                      app.config["OAUTH_SECRET"])
        app.config["TOKEN"]=token
  
    result = users.Users().getUser(target, app.config["OAUTH_KEY"], app.config["OAUTH_SECRET"], app.config['TOKEN'])
    userJSON = json.dumps(result)
    
    return render_template('user.html',
                           target_url=target,
                           userJSON=userJSON,
                           resultsJSON=result,
                           settings=settings)

@app.route('/users/memberships/<userId>')
def UserMemberships(userId=None):
    """
    Return User Memberships Collection
    """
    paginateId = request.args.get('paginateId', None)

    print("USER_ID: %s" % userId)
    print("paginateId: %s" % paginateId)
    
    settings = {'settings':app.config}
    target = app.config["TARGET_URL"] + app.config["USER_MEMBERSHIPS_PATH"]
    #insert courseID into target

    target = target.replace("<userId>", userId)

    if paginateId is None:
        # This is only used by the visit_form on the index page.
        print("paginateId = None: Using configured users_path.")
    else:
        print("paginateId = %s" % paginateId)
        target = (target[:(target.rfind('=')-len(target))])+"="+paginateId

    print ("Altered target: %s" % target)

    #check authZ
    if (app.config["TOKEN"] == ""):
        print("TOKEN NOT SET")
        authtarget = app.config["TARGET_URL"]
        auth_session = auth.AuthToken(authtarget,
                                      app.config["CERT_PATH"])
        token = auth_session.getToken(authtarget, 
                                      app.config["OAUTH_KEY"], 
                                      app.config["OAUTH_SECRET"])
        app.config["TOKEN"]=token
    result = memberships.Memberships().getUserMemberships(target, app.config["OAUTH_KEY"], app.config["OAUTH_SECRET"], app.config['TOKEN'])

    membersJSON = json.dumps(result)

    if (result["paging"]):
        nextpageURL = result["paging"]["nextPage"]
        dataOffset = nextpageURL[(nextpageURL.rfind('=')+1-len(nextpageURL)):]
    else:
        dataOffset = 0
        nextpageURL = None
     
    print("dataOffset: %s" %dataOffset)
    print("dataOffset: %s" % app.config["LIMIT"])

    limitInt = int(app.config["LIMIT"])
    dataOffsetInt = int(dataOffset)

    if (dataOffsetInt <= limitInt):
        dataOffset = None

    print("dataOffset: %s" %dataOffset)

    return render_template('coursememberships.html',
                            target_url=target,
                            membersJSON=membersJSON,
                            resultsJSON=result,
                            pagingJSON=result["paging"],
                            nextpageURL=nextpageURL,
                            dataOffset=dataOffset,
                            settings=settings) 


if __name__ == '__main__':
    app.run()