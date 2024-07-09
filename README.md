# mails-from-csv

a programm for automatically sending group mails and dynamically inserting information from a csv

## installation

these instructions are for linux using bash. for creating an environment using other systems see https://docs.python.org/3/library/venv.html

required python >= 3.9.x

1. create a virtual environment with `python3 -m venv .venv`
2. enter the environemt with `source .venv/bin/activate`
3. install the depenencies into a virtual environment with `python3 -m pip install -r requirements.txt`
4. create the .env file from the provided sample_dotenv file and provide the necessary data

## run

the program reads a .csv file and sends mails to each entry. the csv file needs at least one column with the mail adress. the name of this column needs to be provided as an argument to the program. the .csv file should be comma seperated.

the mail text to be send out should be written in a text file. the path to that file needs to be provided as an argument. in the text file columns names from the .csv file can appear in curly braces like so: {Name}. they will then be exchanged for the corresponding data in the mail that is sent out.

Example usage:

`python3 main.py --csv="data/list_members.csv" --mail_column="E-mail" --template="mail_text.txt" --subject="Wichtig! Bietrunde Spörgelhof eG" --bcc="my_mail@xxx.com"`