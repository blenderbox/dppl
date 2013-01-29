#
# Cookbook Name:: pxlpng
# Recipe:: default
#
# Copyright 2012, Blenderbox
#
# All rights reserved - Do Not Redistribute
#

ENV['LC_ALL'] = "en_US.utf8"

include_recipe "postgresql::server"
include_recipe "postgresql::ruby"
