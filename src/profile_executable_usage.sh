#!/bin/bash
set -e

pstmpfs=/tmp/pstmpfs
mkdir -p $pstmpfs
psinfo=$pstmpfs/psinfo
pstmp=$pstmpfs/pstmp

cleanup() {
	rm -f $pstmp $psinfo
	sync
	sleep 2
	sudo umount $pstmpfs
}

sudo mount -t tmpfs -o size=10m tmpfs $pstmpfs
trap cleanup EXIT SIGINT SIGKILL

declare -A all_pstimes=
rm -f $psinfo
while [ true ]; do
	sleep 1s

	ps -eo etime,cputime,command | tail -n +2 | grep -v '\[\|\]' | grep -v '\-bash' > $pstmp
	while read entry; do
		etime=$(echo $entry | awk {'print $1'})
		ctime=$(echo $entry | awk {'print $2'})
		fullpath=$(which $(echo $entry | awk {'print $3'})| cat -)
		if [ -n "$fullpath" ]; then
			all_pstimes[$fullpath]="$etime,$ctime"
		fi
	done < $pstmp

	for path in "${!all_pstimes[@]}"; do
		echo "$path,${all_pstimes[$path]}" >> $psinfo
	done
done
