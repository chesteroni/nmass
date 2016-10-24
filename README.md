##nmass - massive enumeration and penetration

###What does nmass do?
nmass consumes the results of masscan tool used to do massive TCP scans of large networks and for each result it tries to perform detailed enumeration or simple penetration of that host/port combination

For example imagine that you have an XML result with 10000 opened ports on some few thousands of hosts. Grepping and enumerating manually would be a tremendous effort. With nmass you can do simply:
```
cat result.xml | python nmass.py 
```

The command above will detect every plugin in nmass and would first check whether the plugin is appropriate for the nmass result (e.g. smtp is appropriate for port 25 but not for 3306) and then would fire some enumeration and simple penetration as defined in yaml configuration per the module.

###Why another tool?
Imagine that you have to perform the overall assessment of the large network and detect some low hanging fruits. Wouldn't it be perfect to adjust some configuration and then to fire single, customisable tool able to detect all the exposed ftp servers allowing for anonymous upload, web servers exposing .htaccess or open relay SMTP?

There are plenty of tools out there with nice frontend and a ton of plugins which are hard to customise and pick.

With nmass you can run scan and attack from the crontab with very little effort.
E.g. you can easy scan for few important vulnerabilities and writing new plugins is a very simple task.

###Usage
nmass takes the input file (default is stdin) and fires all the plugins placed in scripts directory. Plugins use configuration available in config directory.

Example usage:

Running all the plugins on the file.xml piped to the nmass
```
cat file.xml | python nmass.py
```

Running all the classes of mysql, spoof and relay classes from smtp and all the classes from ssh module. Output results (if any) in CSV format.
```
python nmass.py --inmass=/path/to/file --intype=xml --scripts=mysql,smtp/spoof,smtp/relay,ssh --out=csv
```
