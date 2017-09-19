#!/bin/sh

test -n "$DEBUG" && set -x
unset CDPATH
name="`readlink -f $0`"

uni_session=17s2
full_class=COMP2041


dir=$uni_session-$full_class-ass1-supplied-files
repo_url=gitlab@gitlab.cse.unsw.EDU.AU:$uni_session$full_class/$dir.git

rm -rf $dir
git init $dir
chmod 700 $dir
#rsync -a examples/ $dir/examples/
rsync pypl.pl $dir/
cat >$dir/.gitignore <<eof
examples/
core
vgcore.*
*~
*.swp
*.pyc
__pycache__
*.zip
eof
cat >$dir/README.md <<eof
COMP[29]041 assignment 1
http://www.cse.unsw.edu.au/~cs2041/assignments/pypl
eof
cat >$dir/diary.txt <<eof
13/09/17    18:00   18:15   put the first real entry in diary.txt (delete this line!)
eof
for i in `iota 00 04`
do
    echo "#!/usr/bin/python3" >$dir/demo$i.py
    echo "# put your demo script here" >>$dir/demo$i.py
    echo "#!/usr/bin/python3" >$dir/test$i.py
    echo "# put your test script here" >>$dir/test$i.py
done
cd $dir
chmod 700 *.py
chmod 600 *.txt
rm -f examples/*/*.sample
git remote add origin $repo_url
git add .
git commit -m 'files supplied to start the assignment'

echo https://gitlab.cse.unsw.edu.au/dashboard/groups create $uni_session$full_class
echo https://gitlab.cse.unsw.edu.au/groups/$uni_session$full_class create $dir
echo cd $dir
echo git push -u origin master
