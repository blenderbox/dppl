#!/bin/bash
proj="dppl"

function db {
    local py=`which python`

    echo "---"
    echo "Updating local_settings.py"
    echo "---"
    cp "source/local_settings.py.example" "source/local_settings.py";
    read -p "What is your mysql username? " username
    read -s -p "What is your mysql password? " password
    sed -i "s/'PASSWORD': \"root\"/'PASSWORD': \"${password}\"/g" "source/local_settings.py"
    echo ""
    echo ""

    echo "---"
    echo "Creating Database"
    echo "---"
    mysql -u $username -p$password -e "CREATE DATABASE ${proj};"
	 $py "source/manage.py" syncdb --migrate --noinput
	 $py "source/manage.py" createsuperuser
}

function bootstrap {
	 echo "---"
	 echo "Checking for Jpeg support"
	 echo "---"
	 local libjpeg="`whereis libjpeg`"
	 if [ "$libjpeg" = "" ]; then
		 echo "It seems that you don't have libjpeg installed, would you like to continue anyway?"
		 select yn in "Yes" "No"; do
			case $yn in
				Yes ) break;
				No ) 
					echo ""
					echo "You need to install libjpeg before going any further:"
					echo "    sudo apt-get install libjpeg libjpeg-dev"
					echo "If you think you've already installed it, try:"
					echo "    pip uninstall pil"
					echo "Then add these symlinks:"
					echo "(substitute 'i386' for 'x84_64' where necessary)"
					echo "    sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/"
					echo "    sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/"
					echo "    sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/"
					echo "And then:"
					echo "    pip install pil"
					echo "Finally, re-run this script to finish the setup."
					echo ""
					exit;
	else
		echo "Libjpeg installed."
	fi

	 echo ""
    echo "---"
    echo "Installing Packages"
    echo "---"
    pip install -r "requirements.pip";
    echo ""

    echo "Do you want to use mysql?"
    select yn in "Yes" "No"; do
        case $yn in
            Yes ) db; break;;
            No ) break;;
        esac
    done

    echo ""
    echo "Finished."
    echo ""
}

function myhelp {
    echo ""
    echo "To install virtualenv, check this out: http://www.doughellmann.com/docs/virtualenvwrapper/"
    echo ""
    echo "After installing, run:"
    echo "    mkvirtualenv ${proj} --no-site-packages && workon ${proj}"
    echo ""
    echo "Then run this script again."
    echo ""
}

echo "Are you currently using your virtualenv? "
select yn in "Yes" "No"; do
    case $yn in
        Yes ) bootstrap; break;;
        No ) myhelp; exit;;
    esac
done
