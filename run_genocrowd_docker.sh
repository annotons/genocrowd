#! /bin/bash

echo "Removing python cache ..."
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

# Create config file
dir_genocrowd="/genocrowd"
config_template_path="$dir_genocrowd/config/genocrowd.ini.template"
config_path="$dir_genocrowd/config/genocrowd.ini"
if [[ ! -f $config_path ]]; then
    # If the file exists it probably means it was mounted -> don't touch it
    cp $config_template_path $config_path

    # Convert env to ini entry
    printenv | egrep "GENOCROWD_" | while read setting
    do
        section=$(echo $setting | egrep -o "^GENOCROWD[^=]+" | sed 's/^.\{5\}//g' | cut -d "_" -f 1)
        key=$(echo $setting | egrep -o "^GENOCROWD[^=]+" | sed 's/^.\{5\}//g' | sed "s/$section\_//g")
        value=$(echo $setting | egrep -o "=.*$" | sed 's/^=//g')
        # crudini --set ${config_path} "${section}" "${key}" "${value}"
        python3 config_updater.py -p $config_path -s "${section}" -k "${key}" -v "${value}"
        $cmd

    done
fi

if [[ "$GENOCROWD_MODE" == "dev" ]]; then
    echo "Rebuilding js in dev mode..."
    npm run -d dev &
    cp docker/uwsgi_dev.ini /etc/uwsgi/uwsgi.ini
else
    cp docker/uwsgi.ini /etc/uwsgi/uwsgi.ini
fi

echo "Starting genocrowd ..."
/usr/bin/supervisord