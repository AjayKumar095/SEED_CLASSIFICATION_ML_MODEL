from flask import render_template, request, Flask
from main.ModelComponents import DataBase
from utils.Helper import load_model
from utils.logger import logging
import sqlite3 as sql
import warnings
import os
warnings.filterwarnings('ignore')

app=Flask(__name__)
app.secret_key='dfnsd4389knxck%$%^HGNBvhfbahdscb^%^%636478jdfbjdbj8734jbHJVHVFDV'




@app.route('/')
def index():
    try:
        logging.info('Showing home page.')
        return render_template('index.html')
    except FileNotFoundError as e:
        logging.info(e)
        return f"""<h1><center>404 ERROR</center></h1><br><p><center>{e}</center></p>"""
    

@app.route('/predict', methods=["POST", "GET"])
def predict():
    try:
        Canadian=['Canadian', 'Canadian wheat is a collective term that encompasses several varieties of wheat grown across Canada, including hard red spring wheat and soft red winter wheat. These varieties are renowned for their high protein content and excellent milling and baking qualities. Canadian wheat is prized in international markets for its consistent quality and versatility in various culinary applications, from breads and pastries to noodles and cereals.']
        Rosa=['Rosa', 'Rosa wheat, another variety of Triticum aestivum, is known for its distinctive reddish hue and robust characteristics. It is often preferred for its resilience to diseases and pests, making it a reliable choice for sustainable farming practices. Rosa wheat grains are medium to large in size and are utilized in both bread and pasta production, offering a balance of texture and flavor.']
        kama=['Kama',"Kama wheat, also known as Triticum aestivum, is a common variety cultivated primarily in Europe and North America. It is valued for its high yield potential and adaptability to various growing conditions. Kama wheat typically produces medium-sized grains that are well-suited for bread-making due to their good gluten content and baking qualities."]
        if request.method=="POST":
           logging.info('Collecting Form Data')
           Area=request.form.get('Area')    
           Perimeter=request.form.get('Perimeter')
           lengthOfKernel=request.form.get('lengthOfKernel')
           widthOfKernel=request.form.get('widthOfKernel')
           compactness=request.form.get('compactness')
           asymmetryCoefficient=request.form.get('asymmetryCoefficient')
           lengthOfKernelGroove=request.form.get('lengthOfKernelGroove')
           
           data_to_predict=[[Area, Perimeter, compactness, lengthOfKernel,
                             widthOfKernel, asymmetryCoefficient, lengthOfKernelGroove]]
           logging.info(f'Form Data collected: {data_to_predict}')
           
           model_path=os.path.join('artifacts', 'Model', 'SVC_model.pkl')
           model=load_model(model_path)
           logging.info('Loadind Modal')
           prediced_value=model.predict(data_to_predict)
           logging.info(f'Predicting new value: {prediced_value}')
   
                                  
           data_tuple=( float(Area),  float(Perimeter),  float(compactness),  float(lengthOfKernel),
                              float(widthOfKernel),  float(asymmetryCoefficient), float(lengthOfKernelGroove),  int(prediced_value[0]))
           
           
           insert_new_data(data=data_tuple)
           if prediced_value == 1:
               return render_template('index.html', predictedvalue=kama)
           
           elif prediced_value==2:
               return render_template('index.html', predictedvalue=Rosa)
            
           elif prediced_value==3:
               return render_template('index.html', predictedvalue=Canadian)
            
           else:
               return render_template('index.html')
            

    except Exception as e:
        logging.info(e)
        return f"""<h1><center>500 ERROR</center></h1><br><p><center>{e}</center></p>"""

def insert_new_data(data:tuple):
    try:
        ## Database Config
        logging.info('Inserting new data points in database.')
        database=DataBase().get_dataBase_path()
        connection=sql.connect(database)
        cursor=connection.cursor()
        
        table_name='Seed_Data_'
        logging.info('Running the sql query.')
        sql_insert_query = f"INSERT INTO {table_name} VALUES {data}"
        cursor.execute(sql_insert_query)
        connection.commit()
        connection.close()
        logging.info('Inserting new data points in database completed.')
        return
    except Exception as e:
        logging.info(f'Error Occure While Inserting New Data: ERROR:- {e}')    
    

if __name__=="__main__":
    app.run(debug=True)