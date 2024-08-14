import csv
import sys

def create_info(name , email):  
    with open("data.csv" , "a" , newline='') as file:
        writer = csv.DictWriter(file , fieldnames= ["Name", "Email" , "Password"])
        writer.writeheader()
        writer.writerow({"Name":name , "Email" :email})
        
        