# CapstoneProject
This repository contains UALR Computer Science Capstone Project for Spring 2020. Our team members include Temuulen Zolbayar, Zezhang Lin, and Jugal Patel.

## To get this project started with PyCharm IDE, follow the step-by-step instructions below:
1. Open PyCharm IDE and select "Get from Version Control".
<img width="775" alt="Screen Shot 2020-04-22 at 10 08 59 AM" src="https://user-images.githubusercontent.com/40209641/80295019-89e8b580-8734-11ea-9cba-95f21d62b2ad.png">

2. Make sure the Version Control field is "Git" and Project URL and Directory matches the below, then hit Clone. 
<img width="576" alt="Screen Shot 2020-04-22 at 10 09 59 AM" src="https://user-images.githubusercontent.com/40209641/80295021-92d98700-8734-11ea-944d-b8ae04d7558f.png">

3. When PyCharm opens the cloned project, open the built-in terminal. 
<img width="1277" alt="Screen Shot 2020-04-22 at 10 14 23 AM" src="https://user-images.githubusercontent.com/40209641/80295025-98cf6800-8734-11ea-89d8-c9724116410d.png">

4. Install python3.8 as it is necessary for this project.
* https://www.python.org/downloads/

5. Type `python3.8 -m venv venv` in the built-in terminal of PyCharm to activate the virtual environment.

6. Migrate the changes to the Django project.  
* Type `python3.8 manage.py migrate` in the built-in terminal.  

7. Create a Django Superuser to be able to log into the Project's Admin Site.  
* Type `python3.8 manage.py createsuperuser` in the built-in terminal.  

8. Run the server and go to `http://127.0.0.1:8000/admin/` to log in with the credentials of Superuser created in Step 7. Create a new addition to `Users` to be able to log into the ADTAA project site.

9. Run the server and go to `http://127.0.0.1:8000/ADTAA/` and you should see the below login page of ADTAA: 
<img width="1207" alt="Screen Shot 2020-04-22 at 10 15 49 AM" src="https://user-images.githubusercontent.com/40209641/80295028-9e2cb280-8734-11ea-8b0e-5f30d93cbfd2.png">
