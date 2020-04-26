### Deployment to PytonAnywhere (Bash Console Commands)
* `git clone https://github.com/txzolbayar/CapstoneProject`
* `mkvirtualenv --python=/usr/bin/python3.8 venv`
* `pip install django`

## Add New Web App
1. Create a domain name to the web app, users have a choice of making their own with payment or use the free one.
2. Select a Python Web framework
* `Manual configuration`
3. Select a Python Version
* `Python 3.8`
4. Set Virtualenv in Web App settings
* `/home/tzolba/.virtualenvs/venv`
5. Change the WSGI configuration file under Code in Web App settings
<img width="796" alt="Screen Shot 2020-04-25 at 9 14 26 PM" src="https://user-images.githubusercontent.com/40209641/80295609-ccf95780-8739-11ea-858c-ea8ccf2006ba.png">

6. Change allowed urls in `/home/tzolba/CapstoneProject/teamproject/teamproject/settings.py` in Files
<img width="435" alt="Screen Shot 2020-04-25 at 9 16 32 PM" src="https://user-images.githubusercontent.com/40209641/80295652-2b263a80-873a-11ea-96ab-1716663cb877.png">

7. Tell PythonAnywhere how to handle web app's static files by adding static root to `/home/tzolba/CapstoneProject/teamproject/teamproject/settings.py` in Files
<img width="596" alt="Screen Shot 2020-04-25 at 9 19 20 PM" src="https://user-images.githubusercontent.com/40209641/80295691-73455d00-873a-11ea-8093-21f8bd0a775e.png">

8. Go back to Bash console and change directory until `/home/tzolba/CapstoneProject/teamproject` then add static files with command
* `python manage.py collectstatic`

9. Add static files to Static in Web App settings like below
<img width="619" alt="Screen Shot 2020-04-25 at 9 25 30 PM" src="https://user-images.githubusercontent.com/40209641/80295804-5eb59480-873b-11ea-81a4-4489c2edd9e3.png">
 
10. Reload the settings for the web app in Web App settings like below
<img width="423" alt="Screen Shot 2020-04-25 at 9 25 48 PM" src="https://user-images.githubusercontent.com/40209641/80295807-62491b80-873b-11ea-9d76-de4b68ebfbd3.png">

11. Go to Web App to see it deployed and available
* http://tzolba.pythonanywhere.com/ADTAA/
