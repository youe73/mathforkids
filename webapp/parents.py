from flask import Blueprint, render_template, request, url_for, flash, redirect
from webapp.forms import RegisterKidsForm, CreateAssignmentCalculationForm, CreateAssignmentTextForm, CreateModuleForm, EditAssignmentCalculationForm
from webapp.models import Users, Registerkids, Modules, Assignmentcalc, Assignmenttext
from flask_login import login_user, current_user, logout_user, login_required
from webapp import db

parents = Blueprint('parents',__name__)


@parents.route('/',methods=['GET','POST'])
def home():         
    enrolled =""
    if current_user.is_authenticated:
        print("authenticated" , current_user.id) 
        print(current_user)               
        enrolled = db.session.query(Registerkids, Users).outerjoin(Users, Registerkids.user_id==Users.id).filter(Registerkids.user_id==current_user.id).all()
        print("query results ",enrolled)        
          
    return render_template('home.html', title='Home', enrolled = enrolled, user = current_user)

@parents.route('/registerkids', methods=['GET','POST'])
def registerkids():
    if current_user.is_authenticated:
        print("authenticated" , current_user.id)
    form = RegisterKidsForm()    
    if form.validate_on_submit():
        kids = Registerkids(kidsusername=form.username.data, kidspassword=form.password.data, age=form.age.data) 
        db.session.add(kids)        
        db.session.add(current_user)
        current_user.registerkids.append(kids)
        db.session.commit()
        flash('You have successfully registered your kid', 'success')
        return redirect(url_for('parents.home'))
    return render_template('registerkids.html', form=form)

@parents.route('/createmodule/<int:id>', methods=['GET','POST'])
def createmodule(id):   
    if current_user.is_authenticated:
        print("authenticated" , current_user.id)  
        moduledisplay = "" 
        path = ""   
        form = ""                         
        # check if kids are registered if not redirect
        reguserkid = db.session.query(Registerkids.id, Users).join(Users, Users.id == Registerkids.user_id).filter(Registerkids.user_id==current_user.id).all()
        print("regkid", reguserkid)
        id_regkid = 0
        for reg in reguserkid:
            id_regkid = reg.id        
        if not reguserkid:
            flash('You have not yet registered any kids, please do so first','warning')
            return redirect(url_for('parents.home'))
        existmodule = db.session.query(Modules).filter_by(registerkids_id=id_regkid).all()        
        print("existing module", existmodule)
        if existmodule:
            moduledisplay = existmodule

        if id == 0: 
            path = 'createassignmentcalculation'
        else:
            path = 'assignmenttext'
        
        form = CreateModuleForm()   
        if form.validate_on_submit():            
            getkidid = 0
            kidsusername = ""
            kidspassword = ""
            age = ""
            getlist = db.session.query(Registerkids, Users).outerjoin(Users, Registerkids.user_id==Users.id).filter(Registerkids.user_id==current_user.id).all()
            for ids,u in getlist:
                getkidid = ids.id 
                kidsusername = ids.kidsusername
                kidspassword = ids.kidspassword
                age = ids.age            
            kid = Registerkids.query.filter(Registerkids.id==getkidid).first()
            print("kid id",getkidid)
            print("kid obj ",kid)
            db.session.add(kid)                        
            moduledata = Modules(modulename = form.modules.data)
            db.session.add(moduledata)                   
            kid.moduleid.append(moduledata)       
            db.session.commit()                        
            mid = Modules.query.order_by(Modules.id.desc()).first()                        
            return redirect(url_for('parents.'+path,id=mid.id))   
    else:
        flash('You must be logged in to view pages','warning')
        return redirect(url_for('auth.login'))
    return render_template('createmodule.html', title='Module', form=form ,id=id, moduledisplay=moduledisplay)


@parents.route('/createassignmentcalculation/<int:id>', methods=['GET','POST'])
def createassignmentcalculation(id):
    if current_user.is_authenticated:
        print("authenticated" , current_user.id)                  
        getkidid = 0
        getlist = db.session.query(Registerkids, Users).outerjoin(Users, Registerkids.user_id==Users.id).filter(Registerkids.user_id==current_user.id).all()
        for ids,u in getlist:
            getkidid = ids.id        
        form = CreateAssignmentCalculationForm()
        if form.validate_on_submit():        
            result = calculation_helper(form.field1.data,form.operator.data,form.field2.data) 
            assigncreated = Assignmentcalc(field1=form.field1.data, operator=form.operator.data, field2=form.field2.data,result=result,module_id = id) 
            db.session.add(assigncreated)            
            db.session.commit()
            return redirect(url_for('parents.createassignmentcalculation',id=id))        
        modname = db.session.query(Modules.modulename, Registerkids).outerjoin(Registerkids, Registerkids.id==getkidid).\
            filter(Registerkids.id==Modules.registerkids_id).order_by(Modules.id.desc()).first()
        
        mod = db.session.query(Registerkids,Modules).outerjoin(Modules, Registerkids.id==getkidid).\
            filter(Registerkids.id==Modules.registerkids_id).all()
        print("module list ",mod)
        print("Name module", modname)
        moduleids = 0        
        for reg, mo in mod:
            moduleids = mo.id     
        assignmentlist = db.session.query(Users, Registerkids, Assignmentcalc).filter(Users.id== current_user.id,
            Assignmentcalc.module_id==id,Registerkids.id==getkidid).all() 
    else:
        flash('You must be logged in to view pages','warning')
        return redirect(url_for('auth.login'))

        print("liste ",assignmentlist)
    return render_template("assignmentcalculation.html", form = form, assignmentlist = assignmentlist, modulename = modname)

def calculation_helper(a,operator,b):
    c = 0
    if operator == "0":
        c = a + b
    elif operator == "1":
        c = a - b
    elif operator == "2":
        c = a * b
    else:
        c = a/b
    return c 


@parents.route('/editassignmentcalculationcomplete', methods=['POST'])
def editassignmentcalculationcomplete():
    if current_user.is_authenticated:
        print(current_user.id)        
        if request.method=="POST":
            id = request.form.get("hiddenid")
            print("hidden id ",id)
            updateassignment = db.session.query(Assignmentcalc).filter(Assignmentcalc.id==id).first()
            field1 = request.form.get("editfield1")
            operator = request.form.get("editoperator")
            field2 = request.form.get("editfield2")
            result = calculation_helper(float(field1), operator, float(field2))                   
            
            print(field1)
            print("toupdate ",updateassignment)
            updateassignment.field1 = field1
            updateassignment.operator = operator
            updateassignment.field2 = field2
            updateassignment.result = result
            db.session.commit()
            flash('Update completed','success')
            return redirect(url_for('parents.home'))            
    return render_template('editassignmentcalculationcomplete.html')



@parents.route('/managekids/<int:id>', methods=['GET','POST'])
def managekids(id):
    if current_user.is_authenticated:               
        module = Modules.query.filter(Modules.registerkids_id==id).all()          
        assignment = db.session.query(Assignmentcalc).all()
        kids = Registerkids.query.filter(Registerkids.id==id).first()              
    return render_template("managekids.html", user = current_user, id = id, module = module, kids = kids, assignment= assignment)


@parents.route('/editassignmentcalcselect', methods=['POST'])
def editassignmentcalcselect():
    if current_user.is_authenticated:
        form = EditAssignmentCalculationForm()        
        if request.method=="POST":
            id = request.form.get("selectitem")
            if id is not "0":                
                assign = db.session.query(Assignmentcalc).filter(Assignmentcalc.id==id).all()                 
                choicelist = form.editoperator.choices   
                for attr in assign:  
                    form.hiddenid.default=id                  
                    form.editfield1.default=attr.field1                                        
                    form.editoperator.choices = choicelist               
                    form.editoperator.default= int(attr.operator)  
                    form.editfield2.default=attr.field2                    
                    form.process()                           
            else:
                return redirect(url_for('parents.home'))

    return render_template("editassignmentcalcselect.html", user = current_user, id = id, form = form)





    





