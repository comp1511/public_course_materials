#!/bin/sh

base=$(dirname $(readlink -f $0))
for level in $base/examples/?
do
	cd $level || continue
	for python in *.py
	do
#		echo $level/$python
		chmod 755 "$python"
		"$python" <$base/examples/input enrollments >/tmp/check_examples.py.output || exit 1
		if test -n "$1"
		then
			for version in 3.4 3.6
			do
				python$version "$python" <$base/examples/input enrollments >/tmp/check_examples.py.output.$version
				diff /tmp/check_examples.py.output.$version /tmp/check_examples.py.output && continue
				echo $level/$python not compatible with version $version
				exit 1
			done
		fi
		b=`basename "$python" .py`
		perl="$level/$b.pl"
		if test ! -r "$perl"
		then
			$base/p2p $python >"$perl" 2>/dev/null
			chmod 755 "$perl"
			"$perl" <$base/examples/input enrollments >/tmp/check_examples.pl.output 2>/dev/null || rm -f "$perl" 
			diff /tmp/check_examples.p?.output >/dev/null || rm -f "$perl"
		fi
		if test ! -r "$perl"
		then
			for f in `find ../../code/    ../../tlb/ -name $b.pl`
			do
				cp $f "$perl"
				chmod 755 "$perl"
				"$perl" <$base/examples/input enrollments >/tmp/check_examples.pl.output 2>/dev/null &&
				diff /tmp/check_examples.p?.output >/dev/null &&
				break
				rm -f "$perl"
			done
			if test ! -r "$perl"
			then
				echo "Missing: $level/$python"
				continue
			fi
		fi
		"$perl" <$base/examples/input enrollments >/tmp/check_examples.pl.output &&
		diff /tmp/check_examples.p?.output >/dev/null && continue
		echo $perl
		echo $level/$python
		diff /tmp/check_examples.p?.output |head -20
		exit 1
	done
done