import csv
import re

def create_info(name , email):  
    with open("data.csv" , "a" , newline='') as file:
        writer = csv.DictWriter(file , fieldnames= ["Name", "Email" , "Password"])
        writer.writerow({"Name":name , "Email" :email})

   
def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False
        
