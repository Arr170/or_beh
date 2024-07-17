# DEV MODE:
1. vytvorit venv
2. `pip install -r requirements.txt`
3. `pip install python-dotenv` (jestli se vyskytne prislusna chyba)
4. vytvorit .env soubor:
   - `FLASK_APP = project`
   - `IS_PROD = 0`
   - `ADMIN_MAIL` a `ADMIN_PASS` nastavit si valstni, vytvori se tim pri prvnim spusteni programu administratorsky ucet
   - `SECRET_POST` nastavit vlastni, potom je treba nastavit hodnotu i v kodu ke ctecce
6. `flask run` pro rozbehnuti programu

# PRODUCTION:
1. hosting: mne se vyplatil [render](https://render.com/), postup bude pro nej
2. v nastaveni web servisu pridat github repo (vyplati se pro hotfixy) nebo nahrat samotny kod
3. nastaveni:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `waitress-serve --call 'project:create_app'`
4. v zalozce "Disk" vytvorit uloziste s Mount path "/project/data", tam bude ulozena databaze, stoji to nejake penize navic
5. v zalozce "Enviroment" nastavit:
   - `FLASK_APP = project`
   - `IS_PROD = 1`
   - `ADMIN_MAIL` a `ADMIN_PASS` nastavit si valstni, vytvori se tim pri prvnim spusteni programu administratorsky ucet
   - `SECRET_POST` nastavit vlastni, potom je treba nastavit hodnotu i v kodu ke ctecce
   
