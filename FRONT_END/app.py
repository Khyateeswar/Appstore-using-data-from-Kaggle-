from collections import UserString
from flask import Flask, render_template,request,session,redirect,flash
import psycopg2
import os,sys

con = psycopg2.connect(
    host = "10.17.50.232",
    database = "group_24",
    user = "group_24",
    password = "hfXC9O2kx8OEM",
    port = 5432
)
cur = con.cursor()

app = Flask(__name__)
app.secret_key=os.urandom(30)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/user_signup')
def usr_signup():
    return render_template('user_signup.html')

@app.route('/dev_signup')
def signup():
    return render_template('dev_signup.html')

@app.route('/login_result',methods=['POST'])
def login_result():
    name=request.form.get('name')
    password=request.form.get('password')
    identity=request.form.get('identity')
    if identity=='user':
        cur.execute("""select * from users where user_name = $${}$$ and password = $${}$$""".format(name,password))
        users = cur.fetchall()
        if len(users)==1:
            session['user_id'] = users[0][0]
            flash("Login Successfull!!")
            return redirect('/user_home')
    else:
        cur.execute("""select * from developers where developer_name = $${}$$ and password = $${}$$""".format(name,password))
        users = cur.fetchall()
        if len(users)==1:
            session['dev_id']=users[0][0]
            flash("Login Successfull!!")
            return redirect('/dev_home')
    return redirect('/')

@app.route('/user_signup_result',methods=['POST'])
def usr_signup_result():
    username=request.form.get('username')
    email=request.form.get('emailid')
    password=request.form.get('password')
    cur.execute(""" SELECT * FROM users WHERE email = $${}$$ OR (user_name= $${}$$ AND password = $${}$$); """.format(email,username,password))
    check_unq = cur.fetchall()
    if(len(check_unq)==0):
        cur.execute("""INSERT INTO users (user_name,email,password)  VALUES ($${}$$,$${}$$,$${}$$);""".format(username,email,password))
        con.commit()
        flash(" User Registration Succesfull,Signed Up!!")
        return redirect('/')
    else:
        flash("Registration failed!!!! Try Again")
        return redirect('/user_signup')
        

@app.route('/dev_signup_result',methods=['POST'])
def signup_result():
    devname=request.form.get('devname')
    email=request.form.get('emailid')
    password=request.form.get('password')
    cur.execute(""" SELECT * FROM developers WHERE email = $${}$$ OR (developer_name= $${}$$ AND password = $${}$$); """.format(email,devname,password))
    check_unq = cur.fetchall()
    if(len(check_unq)==0):
        cur.execute("""INSERT INTO developers (developer_name,email,password)  VALUES ($${}$$,$${}$$,$${}$$);""".format(devname,email,password))
        con.commit()
        flash(" Developer Registration Succesfull,Signed Up!!")
        return redirect('/')
    else:
        flash("Registration failed!!!! Try Again")
        return redirect('/dev_signup')

@app.route('/user_home')
def userhome():
    if 'user_id' in session:
        cur.execute("""select app_id,app_name,rating,price,category_name from apps,category where apps.category_id = category.category_id""")
        l = cur.fetchall()
        return render_template('user_home.html',apps_list = l)
    else:
        flash("Session Expired!!")
        return redirect('/')

@app.route('/dev_home')
def developerhome():
    if 'dev_id' in session:
        cur.execute("""select a.app_id,app_name,rating,price,category_name  from (select app_id from developed where developer_id='{}') as a,apps,category
        where a.app_id=apps.app_id and apps.category_id = category.category_id""".format(session["dev_id"]))
        l=cur.fetchall()
        return render_template('dev_home.html',apps_list=l)
    else:
        flash("Session Expired!!")
        return redirect('/')

@app.route('/logout')
def logout():
    if 'dev_id' in session:
        session.pop('dev_id')
        flash("Logged Out!!")
    elif 'user_id' in session:
        session.pop('user_id')
        flash("Logged Out!!")
    else:
        flash("Session Expired!!")
    return redirect('/')


@app.route('/user_profile')
def usr_profile():
    if 'user_id' in session:
        s=session['user_id']
        cur.execute("""select * from users where user_id='{}'""".format(s))
        l=cur.fetchall()
        cur.execute(""" SELECT installs.app_id,app_name FROM installs,apps WHERE user_id = '{}' and installs.app_id = apps.app_id""".format(s))
        list = cur.fetchall()
        return render_template('user_profile.html',input_name=l[0][1],input_emailid=l[0][2],apps_list = list )
    else:
        flash("Session Expired!!")
        return redirect('/')

@app.route('/dev_profile')
def profile():
    if 'dev_id' in session:
        s=session['dev_id']
        cur.execute("""select * from developers where developer_id='{}'""".format(s))
        l=cur.fetchall()
        return render_template('dev_profile.html',input_name=l[0][1],input_emailid=l[0][2])
    else:
        flash("Session Expired!!")
        return redirect('/')



@app.route('/user_editprofile')
def edprofile():
    if 'user_id' in session:
        return render_template('user_editprofile.html')
    else:
        flash("Session Expired!!")
        return redirect('/')

@app.route('/dev_editprofile')
def ed_profile():
    if 'dev_id' in session:
        return render_template('dev_editprofile.html')
    else:
        flash("Session Expired!!")
        return redirect('/')

@app.route('/user_editdoneprofile',methods=['POST'])
def edit_profile():
    username=request.form.get('new_username')
    password=request.form.get('new_password')
    email=request.form.get('new_emailid')
    if 'user_id' in session:
        cur.execute(""" SELECT * FROM users WHERE email = $${}$$ AND (user_name= $${}$$ AND password = $${}$$); """.format(email,username,password))
        check_unq = cur.fetchall()
        if(len(check_unq)==0):
            cur.execute("""UPDATE users SET user_name = $${}$$,password=$${}$$,email=$${}$$ where user_id='{}'}""".format(username,password,email,session['user_id']))
            con.commit()
            flash("EDIT SUCCESFULL!!")
            return redirect('/user_profile')
        else:
            flash("EDIT UNSUCCESFULL!!! TRY AGAIN")
            return redirect('user_editprofile')
    else:
        flash("Session Expired!!")
        return redirect('/')

@app.route('/dev_editdoneprofile',methods=['POST'])
def editprofile():
    username=request.form.get('new_devname')
    password=request.form.get('new_password')
    emailid=request.form.get('new_emailid')
    if 'dev_id' in session:
        cur.execute(""" SELECT * FROM developers WHERE email = $${}$$ AND (developer_name= $${}$$ AND password = $${}$$); """.format(emailid,username,password))
        check_unq = cur.fetchall()
        if(len(check_unq)==0):
            cur.execute("""UPDATE developers SET developer_name =$${}$$,password=$${}$$,email=$${}$$ where developer_id='{}'""".format(username,password,emailid,session['dev_id']))
            con.commit()
            flash("EDIT SUCCESFULL!!")
            return redirect('/dev_profile')
        else:
            flash("EDIT UNSUCCESFULL!!! TRY AGAIN")
            return redirect('dev_editprofile')
    else:
        flash("Session Expired!!")
        return redirect('/')



@app.route('/user_reviews')
def reviews():
    if 'user_id' in session:
        s=session['user_id']
        cur.execute(""" select app_name,review from reviews,apps where user_id='{}' and  apps.app_id = reviews.app_id """.format(s))
        reviews = cur.fetchall()
        return render_template('user_reviews.html',reviews = reviews)
    else:
        flash("Session Expired!!")
        return redirect('/')

@app.route('/user_suggestions')
def sugges():
    if 'user_id' in session:
        s=session['user_id']
        cur.execute(""" select app_id,app_name,rating,price,category_name from apps,category where apps.category_id = category.category_id and app_id in (select app_id from installs,(select user_id from installs, (select app_id from installs where user_id = '{}') as a where a.app_id = installs.app_id and user_id != '{}' ) as b where b.user_id = installs.user_id and app_id not in (select app_id from installs where user_id = '{}'))""".format(s,s,s))
        l = cur.fetchall()
        return render_template('user_suggestions.html',apps_list = l)
    else:
        flash("Session Expired!!")
        return redirect('/')


@app.route('/filter_apps')
def fil_apps():
    if 'user_id' in session:
        return render_template('filter_apps.html')
    else:
        flash("Session Expired!!")
        return redirect('/')
def array_literal(s):
    out = '{'
    for i in range(len(s)-1):
        out+=s[i]
        out+=','
    out+=s[len(s)-1]
    out+='}'
    return out 

@app.route('/filterdone',methods=['POST'])
def fil_done():
    if 'user_id' in session:
        category = array_literal(request.form.getlist('category'))
        f_price = request.form.get('f_price')
        t_price = request.form.get('t_price')
        sort = request.form.get('sort')
        if(sort == "Alphabetically Asc"):
            cur.execute("""select app_id,app_name,rating,price,category_name from apps,category where apps.category_id = category.category_id and category_name =any($${}$$) and price >='{}' and price <='{}' order by app_name asc""".format(category,f_price,t_price))
        elif(sort == "Alphabetically Dsc"):
            cur.execute("""select app_id,app_name,rating,price,category_name from apps,category where apps.category_id = category.category_id and category_name = any($${}$$) and price >='{}' and price <='{}' order by app_name desc""".format(category,f_price,t_price))
        else:
            cur.execute("""select app_id,app_name,rating,price,category_name from apps,category where apps.category_id = category.category_id and category_name = any($${}$$) and price >='{}' and price <='{}' order by rating desc""".format(category,f_price,t_price))
        l=cur.fetchall()
        return render_template('user_home.html',apps_list=l)
    else:
        flash("Session Expired!!")
        return redirect('/')

@app.route('/upload_app')
def upload():
    if 'dev_id' in session:
        return render_template('upload_app.html')
    else:
        flash("Session Expired!!")
        return redirect('/')

@app.route('/search',methods=['POST'])
def search():
    if 'user_id' in session:
        s=session['user_id']
        search = request.form.get("search")
        cur.execute("""select app_id,app_name,rating,price,category_name from apps,category where apps.category_id = category.category_id and app_name = $${}$$""".format(search))
        l=cur.fetchall()
        cur.execute(""" insert into search_history(user_id,search) values ('{}',$${}$$)""".format(s,search))
        con.commit()
        return render_template('user_home.html',apps_list = l)
    else:
        flash("Session Expired!!")
        return redirect('/')

@app.route('/user_searchhistory')
def history():
    if 'user_id' in session:
        s=session['user_id']
        cur.execute(""" select search from search_history where user_id = '{}' order by search_id asc""".format(s))
        l=cur.fetchall()
        return render_template('user_searchhistory.html',search_history = l)
    else:
        flash("Session Expired!!!")
        return redirect('/')


@app.route('/user_app_page/<id>')
def apppage(id):
    if 'user_id' in session:
        s=session['user_id']
        check = 0
        installed = 0
        cur.execute("""select * from installs where user_id = '{}' and app_id='{}'""".format(s,id))
        l = cur.fetchall()
        if(len(l)==0):
            installed = 0
        else:
            installed =1
        cur.execute(""" select * from reviews where user_id = '{}' and app_id = '{}'""".format(s,id))
        l=cur.fetchall()
        if(len(l)==0):
            check = 0
        else:
            check =1
        cur.execute(""" select app_name,size,rating,price,category_name,cont_rating,num_lang,licensed,app_desc from apps,category where apps.category_id = category.category_id and app_id = '{}' """.format(id))
        l=cur.fetchall()
        name = l[0][0]
        size = l[0][1]
        rating = l[0][2]
        price = l[0][3]
        category = l[0][4]
        cont_rating = l[0][5]
        num_lang = l[0][6]
        licensed = l[0][7]
        if(licensed ==1):
            licensed = 'yes'
        else:
            licensed = 'no'
        app_desc = l[0][8]
        cur.execute(""" select user_name,review from reviews,users where app_id = '{}' and users.user_id = reviews.user_id """.format(id))
        rev = cur.fetchall()
        return render_template('user_app_page.html',review = rev,name=name,size=size,rating = rating,price =price,category = category,cont_rating = cont_rating,num_lang = num_lang,app_desc = app_desc,license = licensed,check = check,installed = installed,id=id)
    else:
        flash("Session Expired!!!")
        return redirect('/')

@app.route('/dev_app_page/<id>')
def dev_page(id):
    if 'dev_id' in session:
        s=session['dev_id']
        cur.execute(""" select app_name,size,rating,price,category_name,cont_rating,num_lang,licensed,app_desc from apps,category where apps.category_id = category.category_id and app_id = '{}' """.format(id))
        l=cur.fetchall()
        name = l[0][0]
        size = l[0][1]
        rating = l[0][2]
        price = l[0][3]
        category = l[0][4]
        cont_rating = l[0][5]
        num_lang = l[0][6]
        licensed = l[0][7]
        if(licensed ==1):
            licensed = 'yes'
        else:
            licensed = 'no'
        app_desc = l[0][8]
        cur.execute(""" select user_name,review from reviews,users where app_id = '{}' and reviews.user_id = users.user_id""".format(id))
        review=cur.fetchall()
        cur.execute(""" select user_name from installs,users where app_id = '{}' and users.user_id = installs.user_id""".format(id))
        users=cur.fetchall()
        return render_template('dev_app_page.html',name = name,size = size,rating=rating,price= price,category = category,cont_rating = cont_rating,num_lang = num_lang,license = licensed,app_desc = app_desc,review = review,users = users,id=id)
    else:
        flash("Session Expired!!")
        return redirect('/')



@app.route('/install/<id>')
def install(id):
    if 'user_id' in session:
        s=session['user_id']
        cur.execute(""" insert into installs(user_id,app_id)  values ('{}','{}')""".format(s,id))
        con.commit()
        return redirect('/user_app_page/'+id)
    else:
        flash("Session Expired!!")
        return redirect('/')

@app.route('/uninstall/<id>')
def uninstall(id):
    if 'user_id' in session:
        s=session['user_id']
        cur.execute(""" delete from installs where user_id = '{}' and app_id = '{}'""".format(s,id))
        con.commit()
        return redirect('/user_app_page/'+id)
    else:
        flash("Session Expired!!")
        return redirect('/')


@app.route('/writereview/<id>',methods = ['POST'])
def rev_rat(id):
    if 'user_id' in session:
        s=session['user_id']
        review = request.form.get('review')
        cur.execute("""insert into reviews(user_id,app_id,review) values ('{}','{}',$${}$$)""".format(s,id,review))
        con.commit()
        return redirect('/user_app_page/'+id) 
    else:
        flash("Session Expired!!")
        return redirect('/')


@app.route('/upload_appdone',methods=['POST'])
def upload_result():
    if 'dev_id' in session:
        app_name=request.form.get('app_name')
        size=request.form.get('size')
        price=request.form.get('price')
        category=request.form.get('category')
        license = request.form.get('licensed')
        num_lang = request.form.get('num_lang')
        if(license == "yes"):
            license = 1
        else:
            license = 0
        cur.execute(""" select category_id from category where category_name=$${}$$""".format(category))
        category_id = cur.fetchall()
        cont_rating= request.form.get("cont_rating")
        app_desc = request.form.get('app_description')
        cur.execute("""select app_id from apps where app_name=$${}$$""".format(app_name))
        l=cur.fetchall()
        if len(l)==0:
            cur.execute("""INSERT INTO apps(app_name,rating,price,category_id,size,num_lang,licensed,app_desc,cont_rating)  VALUES ($${}$$,NULL,'{}','{}','{}','{}','{}',$${}$$,$${}$$)""".format(app_name,price,category_id[0][0],size,num_lang,license,app_desc,cont_rating))
            cur.execute("""select app_id from apps where app_name=$${}$$""".format(app_name))
            l=cur.fetchall()
            m=l[0][0]
            cur.execute("""INSERT INTO developed(developer_id,app_id)   VALUES ('{}','{}')""".format(session['dev_id'],m))
            con.commit()
        else:
            flash("An app is already present with this name. Choose another name")
            return redirect('/upload_app')
        return redirect('/dev_home')
    else:
        flash("Session Expired!")
        return redirect('/')

@app.route('/delete_useraccount')
def del_usr():
    if 'user_id' in session:
        s=session['user_id']
        cur.execute(""" delete from users where user_id = '{}'""".format(s))
        con.commit()
        flash("Account deletion successfull!!")
        return redirect('/')
    else:
        flash("Session Expired!!!")
        return redirect('/')


@app.route('/delete_devaccount')
def del_dev():
    if 'dev_id' in session:
        s=session['dev_id']
        cur.execute("""delete from developers where developer_id = '{}'""".format(s))
        con.commit()
        flash("Account deletion successfull!!")
        return redirect('/')
    else:
        flash("Session Expired!!")
        return redirect('/')

if __name__ == "__main__":
    app.run(host="localhost", port=5024, debug=True)

