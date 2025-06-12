import datetime
from multiprocessing.spawn import prepare
from datetime import datetime
from flask import Flask ,request ,redirect,render_template,session
import pymysql
import os
import pandas as pd
import re
path=os.path.dirname(os.path.abspath(__file__))
property_image=path+"/static/property_image"
csv_file=path+"/static/csv"

app=Flask(__name__)
conn=pymysql.connect(host="localhost",user="root",password="sai@54321",db="property_rental")
cursor=conn.cursor()
app.secret_key="owner"


admin_username="admin"
admin_password="admin"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")
@app.route("/admin_login_action",methods=['post'])
def admin_login_action():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == admin_username and password == admin_password:
        session["role"] = 'admin'
        return redirect("/admin_home")
    else:
        return render_template("message.html", message="invalid login details")

@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")

@app.route("/owner_login")
def owner_login():
    return render_template("owner_login.html")

@app.route("/owner_login_action",methods=['post'])
def owner_login_action():
    email=request.form.get("email")
    password=request.form.get("password")
    count=cursor.execute("select * from owners where email='"+str(email)+"' and password='"+str(password)+"'")
    if count > 0:
        owners = cursor.fetchall()
        if owners[0][6] == 'authorized':
            session['owner_id'] = owners[0][0]
            session['role'] = 'owner'
            return render_template("owner_home.html")
        else:
            return render_template("message.html", message="you are not authorized")
    else:
        return render_template("message.html", message="invalid login details")


@app.route("/owner_home")
def owner_home():
    return render_template("owner_home.html")



@app.route("/owner_registration")
def owner_registration():
    return render_template("owner_registration.html")


@app.route("/owner_registration_action",methods=['post'])
def owner_registration_action():
    name=request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    address = request.form.get("address")
    count=cursor.execute("select * from owners where email='"+str(email)+"'")
    if count>0:
        return render_template("message.html",message="duplicate email address")
    count = cursor.execute("select * from owners where phone='" + str(phone) + "'")
    if count > 0:
        return render_template("message.html", message="duplicate phone number")
    cursor.execute("insert into owners(name,email,phone,password,address) values('" + str(name) + "','" + str(email) + "','" + str(phone) + "','" + str(password) + "','" + str(address) + "')")
    conn.commit()
    return render_template("message.html",message="owner register successfully")


@app.route("/view_owner")
def view_owner():
    cursor.execute("select * from owners")
    owners=cursor.fetchall()
    return render_template("view_owner.html",owners=owners)


@app.route("/authorized_owner")
def authorized_owner():
    owner_id=request.args.get("owner_id")
    cursor.execute("update owners set status='authorized' where owner_id='"+str(owner_id)+"'")
    conn.commit()
    return redirect("/view_owner")

@app.route("/unauthorized_owner")
def unauthorized_owner():
    owner_id = request.args.get("owner_id")
    cursor.execute("update owners set status='unauthorized' where owner_id='" + str(owner_id) + "'")
    conn.commit()
    return redirect("/view_owner")






@app.route("/user_login")
def user_login():
    return render_template("user_login.html")

@app.route("/user_login_action",methods=['post'])
def user_login_action():
    email=request.form.get("email")
    password=request.form.get("password")
    count=cursor.execute("select * from users where email='"+str(email)+"' and password='"+str(password)+"'")
    if count>0:
        users = cursor.fetchall()
        session['user_id'] = users[0][0]
        session['role'] = 'user'
        return render_template("user_home.html")
    else:
        return render_template("message.html",message="invalid login details")


@app.route("/user_home")
def user_home():
    return render_template("user_home.html")

@app.route("/user_registration")
def user_registration():
    return render_template("user_registration.html")

@app.route("/user_registration_action" ,methods=['post'])
def user_registration_action():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    address = request.form.get("address")
    count = cursor.execute("select * from users where email='" + str(email) + "'")
    if count > 0:
        return render_template("message.html", message="duplicate email address")
    count = cursor.execute("select * from users where phone='" + str(phone) + "'")
    if count > 0:
        return render_template("message.html", message="duplicate phone number")
    cursor.execute("insert into users(name,email,phone,password,address) values('" + str(name) + "','" + str(email) + "','" + str(phone) + "','" + str(password) + "','" + str(address) + "')")
    conn.commit()
    return render_template("message.html", message="user register successfully")




@app.route("/sales_properties")
def sales_properties():
    return render_template("sales_properties.html")

@app.route("/add_sales_action",methods=['post'])
def add_sales_action():
    owner_id=session['owner_id']
    property_title=request.form.get("property_title")
    property_value = request.form.get("property_value")
    number_of_bedrooms = request.form.get("number_of_bedrooms")
    number_of_bathrooms = request.form.get("number_of_bathrooms")
    area_in_sqft = request.form.get("area_in_sqft")
    address = request.form.get("address")
    price_per_sqrt = request.form.get("price_per_sqrt")
    build_year = request.form.get("build_year")
    parking_space = request.form.get("parking_space")
    residency_type = request.form.get("residency_type")
    city=request.form.get("city")
    summary=request.args.get("summary")
    cursor.execute("insert into sale_properties(property_title,property_value,number_of_bedrooms,number_of_bathrooms,area_in_sqft,address,price_per_sqrt,build_year,parking_space,residency_type,owner_id,city,summary) values('" + str(property_title) + "','" + str(property_value) + "','" + str(number_of_bedrooms) + "','" + str(number_of_bathrooms) + "','" + str(area_in_sqft) + "','"+str(address)+"','"+str(price_per_sqrt)+"','"+str(build_year)+"','"+str(parking_space)+"','"+str(residency_type)+"', '"+str(owner_id)+"','"+str(city)+"','"+str(summary)+"')")
    conn.commit()
    sale_property_id=cursor.lastrowid
    print(sale_property_id)
    pictures=request.files.getlist("pictures")
    for picture in pictures:
        path=property_image +"/"+ picture.filename
        picture.save(path)
        cursor.execute("insert into sale_property_pictures(sale_property_id,pictures) values('"+str(sale_property_id)+"','"+str(picture.filename)+"')")
        conn.commit()
    return render_template("message2.html", message="sales added successfully")


@app.route("/view_sales")
def view_sales():
    if session['role']=='owner':
        owner_id=session['owner_id']
        query="select * from sale_properties where owner_id='"+str(owner_id)+"'"
    else:
        query="select * from sale_properties where status='posted for sale' "
    cursor.execute(query)
    print(cursor.execute(query))
    sale_properties =cursor.fetchall()
    print(sale_properties)
    sale_properties = list(sale_properties)
    sale_properties.reverse()
    return render_template("view_sales.html",sale_properties=sale_properties,get_sale_property_pictures_by_sale_property_id=get_sale_property_pictures_by_sale_property_id,get_owner_by_owner_id=get_owner_by_owner_id,is_request_sent_by=is_request_sent_by)



def get_sale_property_pictures_by_sale_property_id(sale_property_id):
    cursor.execute("select * from  sale_property_pictures where sale_property_id='"+str(sale_property_id)+"' ")
    sale_properties=cursor.fetchall()
    return sale_properties




@app.route("/rental_properties")
def rental_properties():
    return render_template("rental_properties.html")

@app.route("/add_rental_action",methods=['post'])
def add_rental_action():
    owner_id = session['owner_id']

    property_title = request.form.get("property_title")

    property_type = request.form.get("property_type")
    property_value = request.form.get("property_value")
    number_of_bedrooms = request.form.get("number_of_bedrooms")
    number_of_bathrooms = request.form.get("number_of_bathrooms")
    area_in_sqft = request.form.get("area_in_sqft")
    address = request.form.get("address")
    security_deposit = request.form.get("security_deposit")
    city = request.form.get("city")
    cursor.execute( "insert into rental_properties(owner_id,property_title,property_type,property_value,number_of_bedrooms,number_of_bathrooms,area_in_sqft,address,security_deposit,city) values('"+str(owner_id)+"','"+str(property_title)+"','" + str(property_type) + "','" + str(property_value) + "','" + str(number_of_bedrooms) + "','" + str(number_of_bathrooms) + "','" + str(area_in_sqft) + "','" + str(address) + "','"+str(security_deposit)+"','"+str(city)+"')")
    conn.commit()
    rental_property_id = cursor.lastrowid
    print(rental_property_id)
    pictures = request.files.getlist("pictures")
    for picture in pictures:
        path = property_image + "/" + picture.filename
        picture.save(path)
        cursor.execute("insert into rental_property_pictures(rental_property_id,pictures) values('" + str(rental_property_id) + "','" + str(picture.filename) + "')")
        conn.commit()

    return render_template("message2.html", message="rental added successfully")


@app.route("/view_rental")
def view_rental():
    if session['role']=='owner':
        owner_id=session['owner_id']
        query="select * from rental_properties where owner_id='"+str(owner_id)+"'"
        print(query)
    else:
        query="select * from rental_properties where status='posted for rental' "
    cursor.execute(query)
    print(cursor.execute(query))
    rental_properties =cursor.fetchall()
    print(rental_properties)
    rental_properties = list(rental_properties)
    rental_properties.reverse()
    return render_template("view_rental.html",rental_properties=rental_properties,get_rental_property_pictures_by_rental_property_id=get_rental_property_pictures_by_rental_property_id,get_owner_by_owner_id=get_owner_by_owner_id,is_request_sent=is_request_sent)


def get_rental_property_pictures_by_rental_property_id(rental_property_id):
    cursor.execute("select * from  rental_property_pictures where rental_property_id='"+str(rental_property_id)+"' ")
    rental_properties=cursor.fetchall()
    return rental_properties


def get_owner_by_owner_id(owner_id):
    cursor.execute("select * from  owners where owner_id='"+str(owner_id)+"' ")
    owners=cursor.fetchall()
    return owners[0]


@app.route("/send_rental_request")
def send_rental_request():
    rental_property_id=request.args.get("rental_property_id")
    return render_template("send_rental_request.html",rental_property_id=rental_property_id)


@app.route("/send_sale_request")
def send_sale_request():
    sale_property_id=request.args.get("sale_property_id")
    return render_template("send_sale_request.html",sale_property_id=sale_property_id)




@app.route("/send_rental_request_action",methods=['post'])
def send_rental_request_action():
    rental_property_id=request.form.get("rental_property_id")
    print(rental_property_id)
    summary=request.form.get("summary")
    print(summary)
    date = datetime.now()
    user_id = session['user_id']
    cursor.execute("update rental_properties set summary='"+str(summary)+"' where rental_property_id='"+str(rental_property_id)+"'")
    conn.commit()
    cursor.execute("insert into rental_property_request(rental_property_id, summary, date, user_id) values('"+str(rental_property_id)+"', '"+str(summary)+"', '"+str(date)+"', '"+str(user_id)+"') ")
    conn.commit()
    return render_template("message3.html",message="summary added successfully")



@app.route("/send_sale_request_action",methods=['post'])
def send_sale_request_action():
    sale_property_id=request.form.get("sale_property_id")
    print(sale_property_id)
    summary=request.form.get("summary")
    print(summary)
    date = datetime.now()
    user_id = session['user_id']
    cursor.execute("update sale_properties set summary='"+str(summary)+"' where sale_property_id='"+str(sale_property_id)+"'")
    conn.commit()
    cursor.execute("insert into sale_property_request(sale_property_id, summary, date, user_id) values('"+str(sale_property_id)+"', '"+str(summary)+"', '"+str(date)+"', '"+str(user_id)+"') ")
    conn.commit()
    return render_template("message3.html",message="summary added successfully")



@app.route("/sale_applications")
def sale_applications():
    if session['role']=='user':
        sale_property_id=request.args.get("sale_property_id")
        user_id=session["user_id"]
        if sale_property_id == None:
            query="select * from sale_property_request where user_id='"+str(user_id)+"'"
        else:
            query="select * from sale_property_request where user_id='"+str(user_id)+"' and sale_property_id='"+ str(sale_property_id)+"'"

    else:
        sale_property_id=request.args.get("sale_property_id")
        query="select * from sale_property_request where sale_property_id='"+str(sale_property_id)+"'"
    cursor.execute(query)
    sale_property_requests=cursor.fetchall()
    print(sale_property_requests)
    return render_template("sale_applications.html",sale_property_requests=sale_property_requests,get_user_id_by_user_name=get_user_id_by_user_name,get_sale_property_id_by_sale_property_title=get_sale_property_id_by_sale_property_title)





@app.route("/view_request")
def view_request():
    rental_property_id=request.args.get("rental_property_id")
    return render_template("view_request.html",rental_property_id=rental_property_id)

@app.route("/view_request_action",methods=['post'])
def view_request_action():
    rental_property_id=request.form.get("rental_property_id")
    summary=request.form.get("summary")
    date=datetime.datetime.now()
    user_id=session['user_id']
    cursor.execute("insert into rental_property_request(rental_property_id,summary,date,user_id) values('"+str(rental_property_id)+"','"+str(summary)+"','"+str(date)+"','"+str(user_id)+"')")
    conn.commit()
    return render_template("message2.html",message="sending request successfully")



def is_request_sent(rental_property_id):
    user_id=session['user_id']
    count=cursor.execute("select * from rental_property_request where rental_property_id='"+str(rental_property_id)+"' and user_id='"+str(user_id)+"'")
    if count>0:
        return True
    return False

def is_request_sent_by(sale_property_id):
    user_id=session['user_id']
    count=cursor.execute("select * from sale_property_request where sale_property_id='"+str(sale_property_id)+"' and user_id='"+str(user_id)+"'")
    if count>0:
        return True
    return False




@app.route("/rental_applications")
def rental_applications():
    if session['role']=='user':
        rental_property_id=request.args.get("rental_property_id")
        user_id=session["user_id"]
        if rental_property_id== None:
            query="select * from rental_property_request where user_id='"+str(user_id)+"'"
        else:
            query="select * from rental_property_request where user_id='"+str(user_id)+"' and rental_property_id='"+ str(rental_property_id)+"'"

    else:
        rental_property_id=request.args.get("rental_property_id")
        query="select * from rental_property_request where rental_property_id='"+str(rental_property_id)+"'"
    cursor.execute(query)
    rental_property_requests=cursor.fetchall()
    print(rental_property_requests)
    return render_template("rental_applications.html",rental_property_requests=rental_property_requests,get_user_id_by_user_name=get_user_id_by_user_name,get_rental_property_id_by_rental_property_title=get_rental_property_id_by_rental_property_title)




def get_user_id_by_user_name(user_id):
    cursor.execute("select * from  users where user_id='"+str(user_id)+"' ")
    users=cursor.fetchall()
    return users[0]



def get_rental_property_id_by_rental_property_title(rental_property_id):
    cursor.execute("select * from  rental_properties where rental_property_id='"+str(rental_property_id)+"' ")
    rental_properties=cursor.fetchall()
    return rental_properties[0]


def get_sale_property_id_by_sale_property_title(sale_property_id):
    cursor.execute("select * from  sale_properties where sale_property_id='"+str(sale_property_id)+"' ")
    sale_properties=cursor.fetchall()
    return sale_properties[0]




@app.route("/accept_request")
def accept_request():
    rental_property_id = request.args.get("rental_property_id")
    rental_property_request_id=request.args.get("rental_property_request_id")
    cursor.execute("update rental_property_request set status='rental request accepted' where rental_property_request_id='"+str(rental_property_request_id)+"'")
    conn.commit()
    count = cursor.execute("select * from rental_property_request where rental_property_id='"+str(rental_property_id)+"' and status='Applied for Rental'")
    if count>0:
        cursor.execute("update rental_property_request set status='suspended' where rental_property_id='"+str(rental_property_id)+"' and status='Applied for Rental'")
        conn.commit()
        cursor.execute("update rental_properties set status='rented' where rental_property_id='" + str(rental_property_id) + "'")
        conn.commit()
    return redirect("/rental_applications?rental_property_id="+str(rental_property_id))


@app.route("/accept_request_sale")
def accept_request_sale():
    sale_property_id = request.args.get("sale_property_id")
    sale_property_request_id=request.args.get("sale_property_request_id")
    cursor.execute("update sale_property_request set status='sale request accepted' where sale_property_request_id='"+str(sale_property_request_id)+"'")
    conn.commit()
    count = cursor.execute("select * from sale_property_request where sale_property_id='"+str(sale_property_id)+"' and status='Applied for sale'")
    if count>0:
        cursor.execute("update sale_property_request set status='suspended' where sale_property_id='"+str(sale_property_id)+"' and status='Applied for sale'")
        conn.commit()
        cursor.execute("update sale_properties set status='sold' where sale_property_id='" + str(sale_property_id) + "'")
        conn.commit()
    return redirect("/sale_applications?sale_property_id="+str(sale_property_id))













@app.route("/reject_request")
def reject_request():
    rental_property_request_id = request.args.get("rental_property_request_id")
    cursor.execute("update rental_property_request set status='rental request rejected' where rental_property_request_id='" + str(rental_property_request_id) + "'")
    conn.commit()
    return redirect("/rental_applications")


@app.route("/reject_request_sale")
def reject_request_sale():
    sale_property_request_id = request.args.get("sale_property_request_id")
    cursor.execute("update sale_property_request set status='sale request rejected' where sale_property_request_id='" + str(sale_property_request_id) + "'")
    conn.commit()
    return redirect("/sale_applications")



@app.route("/rental_values")
def rental_values():
    return render_template("rental_values.html")

@app.route("/rental_value_action",methods=['post'])
def rental_value_action():
    file=request.files.get("file")
    path =csv_file +"/"+ file.filename

    file.save(path)
    rentals=pd.read_csv(path)
    print(rentals)
    for rental in rentals.values:
        cursor.execute("insert into rental_values(region_name,date,predicted_value) values('"+str(rental[0]).replace("'", "")+"','"+str(rental[1]).replace("'", "")+"','"+str(rental[2]).replace("'", "")+"')")
        conn.commit()

    return render_template("message1.html", message="uploaded successfully")

@app.route("/home_values")
def home_values():
    return render_template("home_values.html")
@app.route("/home_value_action",methods=['post'])
def home_value_action():
    file = request.files.get("file")
    path = csv_file + "/" + file.filename

    file.save(path)
    homes = pd.read_csv(path)
    print(homes)
    for home in homes.values:
        cursor.execute("insert into home_values(region_name,date,predicted_value) values('" + str(home[0]).replace("'","") + "','" + str(home[1]).replace("'", "") + "','" + str(home[2]).replace("'", "") + "')")
        conn.commit()

    return render_template("message1.html", message="uploaded successfully")

@app.route("/check_rental_affordability")
def check_rental_affordability():
    cursor.execute("select distinct(region_name) from rental_values")
    region_names=cursor.fetchall()

    return render_template("check_rental_affordability.html",region_names=region_names)



def check_rent_affordability(region, annual_income, monthly_rent, verbose=True):
    annual_income = float(re.sub(r'[^\d.]', '', annual_income))
    monthly_rent = float(re.sub(r'[^\d.]', '', monthly_rent))

    monthly_income = annual_income / 12
    rent_to_income_ratio = monthly_rent / monthly_income
    if rent_to_income_ratio <= 0.30:
        status = "Affordable"
    elif rent_to_income_ratio <= 0.50:
        status = "Stretching Budget"
    else:
        status = "Not Affordable"
    return status




@app.route("/check_rental_affordability_action",methods=['post'])
def check_rental_affordability_action():
    region=request.form.get("region")
    monthly_rent = request.form.get("monthly_rent")
    annual_income = request.form.get("annual_income")
    status=check_rent_affordability(region,monthly_rent,annual_income)
    return render_template("check_rental_affordability_action.html",status=status)

@app.route("/get_monthly_rent")
def get_monthly_rent():
    region_name = request.args.get("region_name")
    cursor.execute("select * from rental_values where region_name='"+str(region_name)+"' order by date desc")
    rental_values = cursor.fetchall()
    return {"monthly_rent":round(float(rental_values[0][3]),2)}

@app.route("/get_home_value")
def get_home_value():
    region_name = request.args.get("region_name")
    cursor.execute("select * from home_values where region_name='"+str(region_name)+"' order by date desc")
    home_values = cursor.fetchall()
    print(home_values)
    return {"home_value":round(float(home_values[0][3]),2)}

@app.route("/get_affordability_status")
def get_affordability_status():
    region_name = request.args.get("region_name")
    monthly_rent = request.args.get("monthly_rent")
    annual_income = request.args.get("annual_income")
    status = check_rent_affordability(region_name, monthly_rent, annual_income)
    return {"status": status}

@app.route("/get_buy_affordability_status")
def get_buy_affordability_status():
    region_name = request.args.get("region_name")
    home_value = request.args.get("home_value")
    annual_income = request.args.get("annual_income")
    status, prob = check_buying_affordability_status(region_name, float(annual_income), float(home_value))
    return {"status": status}

@app.route("/check_buying_affordability")
def check_buying_affordability():
    cursor.execute("select distinct(region_name) from home_values")
    region_names = cursor.fetchall()
    return render_template("check_buying_affordability.html", region_names=region_names)



@app.route("/check_buying_affordability_action",methods=['post'])
def check_buying_affordability_action():
    region=request.form.get("region")
    home_value = request.form.get("home_value")
    annual_income = request.form.get("annual_income")
    status, prob =check_buying_affordability(region,home_value,annual_income)
    return render_template("check_buying_affordability_action.html",status=status)

def check_buying_affordability_status(region, annual_income, home_price,
                                down_payment_percent=20,
                                interest_rate=0.06,
                                loan_term_years=30,
                                property_tax_rate=0.0125,
                                insurance_per_year=1500,
                                verbose=True):

    # Monthly income
    monthly_income = annual_income / 12

    # Down payment
    down_payment = home_price * (down_payment_percent / 100)

    # Loan amount
    loan_amount = home_price - down_payment

    # Monthly mortgage payment
    monthly_interest_rate = interest_rate / 12
    number_of_payments = loan_term_years * 12
    monthly_mortgage = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / \
                       ((1 + monthly_interest_rate) ** number_of_payments - 1)

    # Property tax monthly
    monthly_property_tax = (home_price * property_tax_rate) / 12

    # Insurance monthly
    monthly_insurance = insurance_per_year / 12

    # Total monthly housing cost
    total_monthly_cost = monthly_mortgage + monthly_property_tax + monthly_insurance

    # Housing-to-Income ratio
    housing_to_income_ratio = total_monthly_cost / monthly_income

    # Affordability
    if housing_to_income_ratio <= 0.30:
        status = "Affordable"
    elif housing_to_income_ratio <= 0.40:
        status = "Stretching Budget"
    else:
        status = "Not Affordable"

        print(f"Region: {region}")
        print(f"Home Price: ${home_price:,.2f}")
        print(f"Down Payment: ${down_payment:,.2f} ({down_payment_percent}%)")
        print(f"Loan Amount: ${loan_amount:,.2f}")
        print(f"Monthly Mortgage Payment: ${monthly_mortgage:,.2f}")
        print(f"Monthly Property Tax: ${monthly_property_tax:,.2f}")
        print(f"Monthly Insurance: ${monthly_insurance:,.2f}")
        print(f"Total Monthly Housing Cost: ${total_monthly_cost:,.2f}")
        print(f"Monthly Income: ${monthly_income:,.2f}")
        print(f"Housing-to-Income Ratio: {housing_to_income_ratio:.2f} ({housing_to_income_ratio*100:.1f}%)")
        print(f"Affordability Status: {status}")

    return status,housing_to_income_ratio

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/Zori")
def Zori():
    return render_template("Zori.html")

@app.route("/zhvi_yoy")
def zhvi_yoy():
    return render_template("zhvi_yoy.html")

@app.route("/ZHVI")
def ZHVI():
    return render_template("ZHVI.html")


from datetime import date

@app.route("/price_prediction")
def price_prediction():
    city = request.args.get("city")
    property_value = request.args.get("property_value")
    if not city:
        return "City parameter is missing in the URL. Example: /price_prediction?city=San Francisco"

    today = date.today()

    query = """
        SELECT predicted_value 
        FROM rental_values 
        WHERE region_name LIKE %s AND date > %s 
        ORDER BY date DESC 
        LIMIT 1
    """
    cursor.execute(query, (f"%{city}%", today))
    result = cursor.fetchone()

    if not result:
        return f"No future data found for city: {city}"

    rounded_price = round(float(result[0]))
    print(f"${rounded_price}")  # This prints only the price like $2462

    return render_template("price_prediction.html", city=city, price=f"${rounded_price}",property_value=property_value)





from datetime import date

@app.route("/price_prediction_sale")
def price_prediction_sale():
    city = request.args.get("city")
    property_value = request.args.get("property_value")
    print("$$$$$$")
    print("property_value")
    if not city:
        return "City parameter is missing in the URL. Example: /price_prediction_sale?city=San Francisco"

    today = date.today()

    query = """
        SELECT predicted_value 
        FROM rental_values 
        WHERE region_name LIKE %s AND date > %s 
        ORDER BY date DESC 
        LIMIT 1
    """
    cursor.execute(query, (f"%{city}%", today))
    result = cursor.fetchone()

    if not result:
        return f"No future data found for city: {city}"

    rounded_price = round(float(result[0]))
    print(f"${rounded_price}")

    return render_template("price_prediction_sale.html", city=city, price=f"${rounded_price}",property_value=property_value)








app.run(debug=True)



