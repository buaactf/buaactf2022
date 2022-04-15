from flask import Flask, request, send_file, abort
from io import BytesIO
import os
import socket
import ftplib

app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
    return send_file('index.html')

@app.route('/static/<path:path>')
def static_files(path):
    file = os.path.join('static', path)
    if os.path.isfile(file):
        return send_file(file)
    else:
        abort(404)

@app.route("/ftpcheck", methods=['POST'])
def ftpcheck():
    ftpaddr = os.environ['FTPADDR']
    # ftpaddr = '127.0.0.1'
    host = request.form.get('host', '')
    if host == '':
        host = ftpaddr
    try:
        if socket.gethostbyname(host) != ftpaddr:
            return f'Only the specified ftp server {ftpaddr} is acceptable!'
    except:
        return 'Something is wrong, maybe host is invalid.'
    file = 'robots.txt'
    fp = BytesIO()
    try:
        with ftplib.FTP(host) as ftp:
            ftp.login("admin","admin")
            ftp.retrbinary('RETR ' + file, fp.write)
    except ftplib.all_errors as e:
        return 'FTP {} Check Error: {}'.format(host,str(e))
    fp.seek(0)
    try:
        with ftplib.FTP(host) as ftp:
            ftp.login("admin","admin")
            ftp.storbinary('STOR ' + file, fp)
    except ftplib.all_errors as e:
        return 'FTP {} Check Error: {}'.format(host,str(e))
    fp.close()
    return 'FTP {} Check Success.'.format(host)

@app.route("/shellcheck", methods=['POST'])
def shellcheck():
    if request.remote_addr != '127.0.0.1':
        return 'Localhost only'
    shell = request.form.get('shell', '')
    if shell == '':
        return 'Parameter "shell" Empty!'
    return str(os.system(shell))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
