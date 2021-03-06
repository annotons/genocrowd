#! /bin/bash

# Paths
dir_genocrowd=$(dirname "$0")
dir_venv="$dir_genocrowd/venv"
dir_node_modules="$dir_genocrowd/node_modules"
activate="$dir_venv/bin/activate"
ntasks=1

function usage() {
    echo "Usage: $0 (-d { dev | prod })"
    echo "    -d     deployment mode (default: production)"
    echo "    -c     celery max parallel tasks (default: 1)"
}

while getopts "hd:c:" option; do
    case $option in
        h)
            usage
            exit 0
        ;;

        d)
            depmode=$OPTARG
        ;;
        c)
            ntasks=$OPTARG
        ;;
    esac
done

case $depmode in
    prod|production|"")
        flask_depmod="production"
        celery_command="celery -A genocrowd.tasks.celery worker -l info"
    ;;
    dev|development)
        flask_depmod="development"
        celery_command="watchmedo auto-restart -d ${dir_genocrowd}/genocrowd --recursive -p '*.py' --ignore-patterns='*.pyc' -- celery -A genocrowd.tasks.celery worker -l info"
    ;;
    *)
        echo "-d $depmode: wrong deployment mode"
        usage
        exit 1
esac

# Exports
export FLASK_ENV=$flask_depmod
export FLASK_APP="app"

echo "Removing python cache ..."
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

if [[ -f $activate ]]; then
    echo "Sourcing Python virtual environment ..."
    source ${dir_venv}/bin/activate
else
    echo "No virtual environment found. Run install.sh first."
    exit 1
fi

# Create config file
config_template_path="$dir_genocrowd/config/genocrowd.ini.template"
config_path="$dir_genocrowd/config/genocrowd.ini"
if [[ ! -f $config_path ]]; then
    cp $config_template_path $config_path
fi

# Convert env to ini entry
printenv | egrep "GENOCROWD_" | while read setting
do
    section=$(echo $setting | egrep -o "^GENOCROWD[^=]+" | sed 's/^.\{5\}//g' | cut -d "_" -f 1)
    key=$(echo $setting | egrep -o "^GENOCROWD[^=]+" | sed 's/^.\{5\}//g' | sed "s/$section\_//g")
    value=$(echo $setting | egrep -o "=.*$" | sed 's/^=//g')
    # crudini --set ${config_path} "${section}" "${key}" "${value}"
    python3 config_updater.py -p $config_path -s "${section}" -k "${key}" -v "${value}"
done

echo "Starting Celery ..."
celery -A genocrowd.tasks.celery worker -Q default -c ${ntasks} -n default -l info
$celery_command
