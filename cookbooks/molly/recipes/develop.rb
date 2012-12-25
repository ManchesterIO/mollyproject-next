molly_user = 'molly'

user molly_user

directory '/opt/molly' do
  action :create
  owner molly_user
  group molly_user
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
