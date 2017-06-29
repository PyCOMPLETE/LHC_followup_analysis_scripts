#!/bin/sh
user=lhcscrub
echo "Give password for $user"
sshfs ${user}@lxplus:/eos /eos
