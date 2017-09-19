# course_materials
COMP[29]041 Course Materials

[htaccess.course_account](htaccess.course_account) serves some content directly.
Most content served by flask http://cgi.cse.unsw.edu.au/~cs2041cflask.cgi
using (Jinja) [templates](templates) + custom code in [scripts/webpages.py](scripts/webpages.py)


# tut-lab Setup

tutlabs are released to students if a file matching this regex exists:
tlb/(\d\d)/(tut|lab)_(questions|answers)_released 
for example tlb/02/lab_answers_released

This access protection for unreleased tut/lab question/answers
is implemented both by rewrite rules in [htaccess.cgi_account](htaccess.course_account)
and code in [scripts/webpages.py](scripts/webpages.py)

# Configuration Variables

[scripts/config.py](scripts/config.py) [scripts/config.sh](scripts/config.s)
should be used to obtain Shell/Python config variables

# Jinja Template Variables

All the ariables [scripts/config.py](scripts/config.py) are available in Jinja templates

Also available are:

* is_tutor - user has authenticated with zid of tutor (see [htaccess.course_account](htaccess.course_account))



# code examples Setup

# GIT Setup

All course materials except exam questions in https://github.com/COMP2041UNSW/course_materials

All lecturers and tutors added to https://github.com/orgs/COMP2041UNSW/teams/17s1
which has write access

COMP2041 also has user account https://github.com/COMP2041/
which be accessed with cs2041 & cs2041cgi ssh keys


A push to https://github.com/COMP2041UNSW/course_materials triggers 2 webhooks
specified at https://github.com/COMP2041UNSW/course_materials/settings/hooks
* http://cgi.cse.unsw.edu.au/~cs2041/cgi/github_pull.cgi 
* http://cgi.cse.unsw.edu.au/~cs2041cgi/cgi/github_pull.cgi 

The CGI script runs [scripts/git_pull.sh](scripts/git_pull.sh)

This authenticates secret supplied via webhook against [.github_secret]()

# New session

Clone https://github.com/COMP2041UNSW/course_materials in class account like this for new session

1) get personal access token from https://github.com/COMP2041/ -> https://github.com/settings/tokens 

 s=17s1
 cd ~/public_html
 git clone https://PERSONAL_ACCESS_TOKEN@github.com/COMP2041UNSW/course_materials $s
 cd $s
 find .|scripts/set_filesystems_permissions

Note session is embedded in [lib/python/cse/course_configuration.py](lib/python/cse/course_configuration.py)
and [scripts/autotest](scripts/autotest)

tutors/.htaccess and tutors/smsfield needed to updated (copied from last session)
after give-install 
