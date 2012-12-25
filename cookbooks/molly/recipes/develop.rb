molly_user = 'molly'

user molly_user

%w(/opt/molly /var/lib/molly /var/log/molly).each do | path |
  directory path do
    action :create
    owner molly_user
    group molly_user
  end
end

python_virtualenv '/opt/molly' do
  owner molly_user
  group molly_user
  action :create
end

bash "Setup Molly" do
  cwd '/tmp'
  user molly_user
  group molly_user
  code <<-EOH
    /opt/molly/bin/pip install -r /vagrant/requirements.txt
    /opt/molly/bin/python /vagrant/setup.py develop
  EOH
end

bash "Run Molly" do
  cwd '/vagrant'
  user 'root'
  group 'root'
  code <<-EOH
    env PYTHONPATH=/vagrant MOLLY_CONFIG=/vagrant/conf/default.conf /opt/molly/bin/mollydebugd
  EOH
end
