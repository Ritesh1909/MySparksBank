from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
#Initialize the database
db = SQLAlchemy(app)
#Create db model
class List(db.Model):
    id = db.Column(db.Integer)
    name = db.Column(db.String(100),  primary_key=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Integer)

class Records(db.Model):
    debitedFrom = db.Column(db.String(100), nullable=False)
    creditedTo = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer) 
    date_created =  db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)   

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/index.html")
def Home():
    return render_template('index.html')   

@app.route("/transact.html/<ID>/<Name>/<Email>/<Balance>")
def transact(ID, Name, Email, Balance):
    Lists = List.query.order_by(List.id)
    return render_template('transact.html', ID = ID, Name = Name, Email = Email, Balance = Balance, Lists=Lists)           

@app.route("/customers.html")
def customers():
    Lists = List.query.order_by(List.id)
    return render_template('customers.html', Lists=Lists)    

@app.route("/record.html")
def test(): 
    records = Records.query.order_by(Records.date_created.desc())   
    return render_template('record.html', records=records) 

@app.route("/info.html/<name>", methods=["GET","POST"])
def record(name):    
    if request.method == "POST":
        Name = request.form.get("Name")
        Amount = request.form.get("Amount")
        updateSender = List.query.get(name)
        updateReceiver = List.query.get(Name)
        if(not Name or not Amount):
            error_statement = "Transaction blocked!!! Enter valid details. "
            return render_template('record.html', error_statement=error_statement) 
        else:
            updateSender.balance = updateSender.balance - int(Amount)
            updateReceiver.balance = updateReceiver.balance + int(Amount)
            # db.session.commit()
            new_record = Records(debitedFrom=name,creditedTo=Name,amount=Amount)
            Statement = "Transaction Completed!!! "
            records = Records.query.order_by(Records.date_created.desc())
            try:
                db.session.add(new_record)
                db.session.commit()
                return render_template('info.html', Statement=Statement, records=records) 
            except:
                return "There was error"   
    else:   
        return render_template('info.html')          

# @app.route("/Enter.html", methods=["GET","POST"])        
# def enter():
#     if request.method == "POST":
#         id = request.form["ID"]
#         name = request.form["Name"]
#         email = request.form["Email"]
#         balance = request.form["Balance"]
#         new_List = List(id=id,name=name,email=email,balance=balance)
#         try:
#             db.session.add(new_List)
#             db.session.commit()
#             return redirect('/Enter.html')
#         except:
#             return "There was error"
#     else:  
#         Lists = List.query.order_by(List.id)          
#         return render_template('Enter.html', Lists = Lists) 