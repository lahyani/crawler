Overview:
======================================
This project has the purpose to retreive data from web page and push the data into database (Firebase)

Installation:
======================================
The project use Firebase as realtime database. Please create a database by following this link:
https://console.firebase.google.com/

Inside <config> directory, copy the file <example.config.yaml> and rename it to config.yaml. Put your credentials in the corresponding field

For security reason you have to define an Email/Password authentification for your database. Use this link where {your_database_id} is the database identifier for your database
https://console.firebase.google.com/project/{your_database_id}/authentication/users

I recommand to instal pip and virtualenv (mkvirualenv on windows plateforme)

To install the project run the command:

pip install -r requirements.txt requirements.dev.txt

The Crawler
======================================
To populate the database for pepsi's facebook page run the command:

python src/crawler.py --uri=crawler/fans_count --page_id=pepsi --plateforme=facebook
Or
You can define a job into a file inside <job> directory then run start_job.py after adding the path to your jobs

config_file = {
    "database" : "./config/config.yaml",
    "jobs" : [
        "./job/bunch_001.yaml",
        "./job/bunch_002.yaml",
    ],
}

The crawler can parse facebook pages to extract fans count and visitors count

You can see the data structure by viewing the image <data/database-structure.png> 

TODO
======================================
- Process  errors and exceptions
- Add documentation
- Build frontend to display data using Vue and VueFire
