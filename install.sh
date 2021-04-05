#!/usr/bin/env bash

DT=""
case "$(uname -s)" in

   Darwin)
     DT="~/.local/share/"
     ;;

   Linux)
     DT="~/.local/share/"
     ;;

   CYGWIN*|MINGW32*)
     DT=$(cygpath ${APPDATA})
     ;;

esac


if [ -z ${DT} ] ; then
    echo "path to renderdoc doesn't exists for this system, you should install it manually"
    exit 1
fi

DT=${DT}"/qrenderdoc/extensions"


if [ ! -d ${DT} ] ; then
    echo "path ${DT} doesn't exists, make sure renerDoc is installed"
    exit 2
fi

cp -R raw_texture_dump ${DT}
