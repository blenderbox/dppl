#
# Cookbook Name:: pxlpng
# Recipe:: default
#
# Copyright 2012, Blenderbox
#
# All rights reserved - Do Not Redistribute
#

db_conn = {
  :host => "localhost",
  :username => "root",
  :password => node['mysql']['server_root_password']
}

node['app']['sites'].each do |site|
  db = data_bag_item('databases', site['database']['name'])
  mysql_database_user db['user'] do
    connection db_conn
    password db['password']
    action :create
  end

  mysql_database_user db['user'] do
    connection db_conn
    database_name db['id']
    password db['password']
    host db_conn['host']
    privileges [:all]
    action :grant
  end

  template "/var/www/pxlpng.com/app/source/settings/passwords.py" do
    source "passwords.py.erb"
    mode 0660
    owner "deploy"
    group "www-data"
    backup false
    variables({
      "username" => db['user'],
      "password" => db['password']
    })
  end

  gem_package "sass" do
    action :install
  end
end
