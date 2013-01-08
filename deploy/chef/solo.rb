root = File.expand_path(File.dirname(__FILE__))

file_cache_path           "/tmp/chef-solo"
data_bag_path             "/tmp/chef-solo/data_bags"
encrypted_data_bag_secret "/tmp/chef-solo/data_bags/key"
cookbook_path             [ "/tmp/chef-solo/site-cookbooks",
                            "/tmp/chef-solo/cookbooks" ]
role_path                 "/tmp/chef-solo/roles"
