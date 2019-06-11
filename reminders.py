from google.cloud import bigquery
client = bigquery.Client()
#--------------------------ADD NEW REMINDER--------------------------------
def addinrem():
      from google.cloud import bigquery
      client = bigquery.Client()
      print("enter with the right formate only")
      print("enter reminder:")
      temp1 = input()
      print("enter Date:YYYY-MM-DD")
      temp2 = input()
      print("enter Time= HH:MM:SS")
      temp3 = input()

      #print(format(temp, temp2,temp3))


      query = """
      INSERT reminder.MyReminder(Reminder, Date, Time)
      VALUES(@remname1,@remname2,@remname3)
      """
      query_params = [
          bigquery.ScalarQueryParameter("remname1", "STRING", temp1),
          bigquery.ScalarQueryParameter("remname2", "DATE", temp2),
          bigquery.ScalarQueryParameter("remname3", "TIME", temp3),
      ]
      job_config = bigquery.QueryJobConfig()
      job_config.query_parameters = query_params
      query_job = client.query(
          query,
          # Location must match that of the dataset(s) referenced in the query.
          location="asia-south1",
          job_config=job_config,
      )  # API request - starts the query

      print("reminder sucessfully inserted")
      
#--------------------Delete a certain reminder by remindar name DOESNT WORK------------------------
def deleteinrem():
      print("enter name of reminder you want to delete")
      temp = input()
      print("sucessfully deleted reminder",temp)
      query = """
          DELETE FROM `reminder.MyReminder`
          WHERE Reminder = @remname;
      """
      query_params = [
          bigquery.ScalarQueryParameter("remname", "STRING", temp),
      ]
      job_config = bigquery.QueryJobConfig()
      job_config.query_parameters = query_params
      query_job = client.query(
          query,
          # Location must match that of the dataset(s) referenced in the query.
          location="asia-south1",
          job_config=job_config,
      )  # API request - starts the query      
      
#------------------------------Search by reminder name-----------------------------------------------------
def checkbyremname(): 
      print("enter name of reminder you'd like to search:")
      temp = input()
      query = """
         SELECT Date,Reminder,Time
          FROM `reminder.MyReminder`
          WHERE Reminder = @remname
          ORDER BY Date DESC;
      """
      query_params = [
          bigquery.ScalarQueryParameter("remname", "STRING", temp),
      ]
      job_config = bigquery.QueryJobConfig()
      job_config.query_parameters = query_params
      query_job = client.query(
          query,
          # Location must match that of the dataset(s) referenced in the query.
          location="asia-south1",
          job_config=job_config,
      )  # API request - starts the query

      # Print the results
      print("'Date'\t 'Reminder'\t 'Time'")
      for row in query_job:
          print("{}:\t{} \t{}".format(row.Date,row.Reminder,row.Time))
      assert query_job.state == "DONE"
      
#--------------------------------Check By todays Date-------------------------------      
def  checkbytoday():
      import datetime
      import pytz
      from datetime import date
      today = date.today()

      d1 = today.strftime("%Y-%m-%d")
      print(d1)
      query = """
         SELECT Date,Reminder,Time
          FROM `reminder.MyReminder`
          WHERE Date = @d_value
          ORDER BY Date DESC;
      """
      query_params = [
          bigquery.ScalarQueryParameter("d_value", "DATE", d1),
      ]
      job_config = bigquery.QueryJobConfig()
      job_config.query_parameters = query_params
      query_job = client.query(
          query,
          # Location must match that of the dataset(s) referenced in the query.
          location="asia-south1",
          job_config=job_config,
      )  # API request - starts the query

      # Print the results
      print("'Date'\t 'Reminder'\t 'Time'")
      for row in query_job:
          print("{}:\t{} \t{}".format(row.Date,row.Reminder,row.Time))

      assert query_job.state == "DONE"  
      
#-----------------------------------list all reminders-------------------------------------------
from google.cloud import bigquery
client = bigquery.Client()
def printlist():
      # Perform a query.
      QUERY = (
          'SELECT Date,Reminder,Time FROM `reminder.MyReminder`')

      query_job = client.query(QUERY)  # API request
      rows = query_job.result()  # Waits for query to finish


      print("'Date'\t 'Reminder'\t 'Time'")
      for row in rows:
        print("{} \t{} \t{} ".format(row.Date,row.Reminder,row.Time))  
  
print("\n\nWelcome to Reminder\n")
choices = 5
cont = 'c'

while cont == 'c':
    choice = 0
    print("\nWhat do you want to do ? (press the corresponding choice no.) \n")
    print("1. Add a new reminder.")
    print("2. Delete a a reminder.")
    print("3. Check for reminder by its name.")
    print("4. Check for a reminder for today.")
    print("5. Print whole reminder list.")
    while choice <= 0 or choice > choices:
        #print(f"\nPlease enter a valid input of choice between 1 and {choices}")
        choice = input()
        try:
            choice = int(choice)
        except ValueError:
            choice = 0
    print("OK \n")
    if choice == 1:
        addinrem()
    elif choice == 2:
        deleteinrem()
    elif choice == 3:
        checkbyremname()
    elif choice == 4:
        checkbytoday()
    else:
        printlist()

    print("Do you want to continue or exit ? (press c to continue)")
    cont = input()
