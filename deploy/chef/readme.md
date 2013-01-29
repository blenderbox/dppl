# <a name="setup"></a> Setup
1. Clone this repository to your computer and checkout the chef branch:
```bash
$ git clone git@github.com:blenderbox/chef-setup.git
$ git checkout chef
```

2. Go into the chef directory. This will initialize the RVM and
   then install the gems. If you don't have RVM installed, [install
   it](https://rvm.io/rvm/install/), then go through the setup process, and
   finally cd out and back into the directory.
```bash
$ cd dppl/deploy/chef
$ gem install knife-solo librarian
```

3. Now install all of the chef cookbooks, which are managed with
   `librarian`.
```bash
$ librarian-chef install
```

4. *Optional*: If you want to use this setup with Vagrant, I've created
   a Vagrantfile to make it smoother:
    * Install the vagrant gem.
    * Start up your new vagrant box.
    * Get the SSH connection string
```bash
$ gem install vagrant
$ vagrant up
```


# <a name="how-to"></a> How To Use
1. Once you've created a vanilla server, you'll want to prepare it for
   chef. You can do this with the `prepare` command. This command
   takes the host information as an argument. Your ssh configuration in a file
   called `vagrant.ssh`, and your host is called `dppl-local`:
```bash
$ knife solo prepare dppl-local -F vagrant.ssh
```
