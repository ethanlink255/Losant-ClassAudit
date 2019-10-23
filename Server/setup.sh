apt update
apt install default-mysql-server python3-pip python3 python3-pip libmariadb-dev libmariadb-dev-compat libpcre3 libpcre3-dev -y
mysql < ./Database/init.sql