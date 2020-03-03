#! /bin/bash

# Paths
dir_genocrowd=$(dirname "$0")
dir_venv="$dir_genocrowd/venv"
dir_node_modules="$dir_genocrowd/node_modules"
activate="$dir_venv/bin/activate"

error=0

function usage() {
    echo "Usage: $0"
}

find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

if [[ -f $activate ]]; then
    echo "Sourcing Python virtual environment ..."
    source ${dir_venv}/bin/activate
else
    echo "No virtual environment found. Run install.sh first."
    error=1
fi

if [[ ! -d $dir_node_modules ]]; then
    echo "No node_modules directory found. Run install.sh first."
    error=1
fi

if [[ ! -f $dir_genocrowd/genocrowd/static/js/genocrowd.js ]]; then
    echo "Javascript not built. Run build.sh first."
    error=1
fi

if [[ $error > 0 ]]; then
    exit 1
fi


# Lint JS
echo "Linting JS files ..."
${dir_node_modules}/.bin/eslint --config ${dir_genocrowd}/.eslintrc.yml "${dir_genocrowd}/genocrowd/react/src/**" && echo "OK" || exit 1

# Lint Python
echo "Linting Python files ..."
flake8 ${dir_genocrowd}/genocrowd ${dir_genocrowd}/tests --ignore=E501,W504 && echo "OK" || exit 1

# Test Python
pytest --cov=. -vv && echo "OK" || exit 1
