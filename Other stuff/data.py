import csv
import re

def create_info(name , email):  
    with open("data.csv" , "a" , newline='') as file:
        writer = csv.DictWriter(file , fieldnames= ["Name", "Email" , "Password"])
        writer.writerow({"Name":name , "Email" :email})
        
        