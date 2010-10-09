# Delicious to Blogger #

Looks up the delicious links I posted recently and generates a blog post for 
blogger from the links.

## Motivation ##

On a weekly basis I save up a bunch of links to my Delicious account. These 
links are like a Zeitgeist of my mind, but they can get lost in the black hole
that Delicious can sometimes be. 

So, in order to perpetuate this Zeitgeist, I thought it would be cool to create
a blog post for the week's links. This script automates this process.

## Requirements ##

There are two main requirements for this tool to work:

1. **Python Delicious API** - [http://code.google.com/p/pydelicious/](http://code.google.com/p/pydelicious/)
2. **GData Blogger API** - [http://code.google.com/apis/blogger/](http://code.google.com/apis/blogger/)

## How it Works ##

I opened the INI config file and ensured the the login information for both
Delicious and Blogger is correct and then saved and closed the file. Next I
added the following command call to my crontab to run once a week on Saturdays
at noon.

    python deliciouspipegreplinkspipeblogger.py -l -v

### Command Line Options ###

    $ python deliciouspipegreplinkspipeblogger.py -h
    
    Usage: deliciouspipegreplinkspipeblogger.py [options] arg
    
    Looks up the delicious links posted recently to your account and generates a
    blog post for blogger from the links.

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -v, --verbose         display and log verbose messages [default]
      -q, --quiet           turns verbosity way down
      -l, --log             write messages to a log file
      -i FILE, --inifile=FILE
                            the configuration file that drives the work

    Requires the pydelicious and blogger data api modules.
    http://code.google.com/p/pydelicious/
    http://code.google.com/apis/blogger/

## Further Information ##

Here are some useful links:

1. [http://www.saltycrane.com/blog/2008/11/python-datetime-time-conversions/](http://www.saltycrane.com/blog/2008/11/python-datetime-time-conversions/)
2. [http://code.google.com/apis/blogger/docs/2.0/reference.html](http://code.google.com/apis/blogger/docs/2.0/reference.html)
3. [http://code.google.com/apis/blogger/docs/1.0/developers_guide_python.html](http://code.google.com/apis/blogger/docs/1.0/developers_guide_python.html)
4. [http://code.google.com/apis/blogger/](http://code.google.com/apis/blogger/)
5. [http://code.google.com/p/pydelicious/](http://code.google.com/p/pydelicious/)
6. [http://www.delicious.com/help/thirdpartytools](http://www.delicious.com/help/thirdpartytools)
7. [http://www.delicious.com/help/api](http://www.delicious.com/help/api)
