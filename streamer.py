import time

logs = [
    '127.0.0.1 - - [22/Feb/2026:22:10:01 +0300] "GET /assets/images/logo.png HTTP/1.1" 200 4523 "https://mysite.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"',
    '192.168.1.105 - - [22/Feb/2026:22:12:45 +0300] "GET /login.php?user=admin\' AND (SELECT 1 FROM (SELECT(SLEEP(5)))a)-- HTTP/1.1" 200 512 "-" "Mozilla/5.0"',
    'Feb 22 22:15:01 cloud-server sshd[1245]: Accepted password for developer from 192.168.1.20 port 54321 ssh2',
    'Feb 22 22:18:33 my-server sshd[25341]: Failed password for invalid user admin from 103.45.12.8 port 56789 ssh2',
    '45.89.23.12 - - [22/Feb/2026:22:25:40 +0300] "GET /../../../../etc/passwd HTTP/1.1" 403 162 "-" "curl/7.81.0"'
]

with open("server_logs.txt", "a") as f:
    for log in logs:
        f.write(log + "\n")
        f.flush() 
        
        time.sleep(7)