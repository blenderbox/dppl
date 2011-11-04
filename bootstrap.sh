#!/bin/bash
proj="dppl"

bold="$(tput bold)"
reset="$(tput sgr0)"
red="$(tput setaf 1)"
yellow="$(tput setaf 3)"
green="$(tput setaf 2)"

function error { echo "${bold}${red}${1}${reset}"; }
function warn { echo "${bold}${yellow}${1}${reset}"; }
function success { echo "${bold}${green}${1}${reset}"; }

function db {
	local py=`which python`

	echo ""
	echo "---"
	warn "Updating local_settings.py"
	echo "---"
	cp "source/local_settings.py.example" "source/local_settings.py";
	read -p "What is your mysql username? " username
	read -s -p "What is your mysql password? " password
	sed -i "s/'PASSWORD': \"root\"/'PASSWORD': \"${password}\"/g" "source/local_settings.py"
	echo ""
	echo ""

	echo "---"
	warn "Creating Database"
	echo "---"
	mysql -u $username -p$password -e "CREATE DATABASE ${proj};"
	$py "source/manage.py" syncdb --migrate --noinput
	$py "source/manage.py" createsuperuser
}

function bootstrap {
	echo ""
	echo "---"
	warn "Checking for Jpeg support"
	echo "---"
	local libjpeg="`whereis libjpeg`"

	if [ "$libjpeg" = "" ]
	then
		 error "It seems that you don't have libjpeg installed, would you like to continue anyway?"
		 select yn in "Yes" "No"
			do
				case $yn in
					Yes )
						break
						;;
					No ) 
						echo ""
						echo "You need to install libjpeg before going any further:"
						echo "    ${bold}sudo apt-get install libjpeg libjpeg-dev${reset}"
						echo "If you think you've already installed it, try:"
						echo "    ${bold}pip uninstall pil${reset}"
						echo "Then add these symlinks:"
						echo "(substitute 'i386' for 'x84_64' where necessary)"
						echo "    ${bold}sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/${reset}"
						echo "    ${bold}sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/${reset}"
						echo "    ${bold}sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/${reset}"
						echo "And then:"
						echo "    ${bold}pip install pil${reset}"
						echo "Finally, re-run this script to finish the setup."
						echo ""
						exit
						;;
				esac
			done
	else
		success "Libjpeg installed."
	fi

	echo ""
	echo "---"
	warn "Installing Packages"
	echo "---"
	pip install -r "requirements.pip";
	echo ""

	echo "${bold}Do you want to use mysql?${reset}"
	select yn in "Yes" "No"
		do
			case $yn in
				Yes )
					db
					break
					;;
				No )
					break
					;;
			esac
	done

	echo ""
	success "Finished."
	echo ""
}

function myhelp {
	echo ""
	echo "To install virtualenv, check this out: http://www.doughellmann.com/docs/virtualenvwrapper/"
	echo ""
	echo "After installing, run:"
	echo "    ${bold}mkvirtualenv ${proj} --no-site-packages && workon ${proj} ${reset}"
	echo ""
	echo "Then run this script again."
	echo ""
}

echo "${bold}Are you currently using your virtualenv?${reset} "
select yn in "Yes" "No"; do
	case $yn in
		Yes )
			bootstrap
			break
			;;
		No )
			myhelp
			exit
			;;
	esac
done
