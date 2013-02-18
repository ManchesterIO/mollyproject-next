APT_PACKAGES = %w(tomcat6)
DIRECTORIES = %w(/opt/solr4 /opt/solr4/data /usr/share/tomcat6-solr)
SYSTEM_SERVICES = %w(tomcat6)

APT_PACKAGES.each do | pkg |
  package pkg do
    action :install
  end
end

execute "apt-get update"

DIRECTORIES.each do | path |
  directory path do
    action :create
    owner 'tomcat6'
    group 'tomcat6'
  end
end

remote_file "/opt/solr4/solr-4.1.0.tgz" do
  action :create_if_missing
  source "http://mirror.ox.ac.uk/sites/rsync.apache.org/lucene/solr/4.1.0/solr-4.1.0.tgz"
  mode 0644
end

execute "expand Solr" do
  cwd '/tmp'
  command 'tar zxf /opt/solr4/solr-4.1.0.tgz && cp -rf solr-4.1.0/example/solr/* /opt/solr4'
  user 'tomcat6'
  group 'tomcat6'
end

execute "add Solr webapp" do
  cwd '/tmp'
  command 'cp solr-4.1.0/example/webapps/solr.war /usr/share/tomcat6-solr/solr.war'
end

cookbook_file "/etc/tomcat6/Catalina/localhost/solr.xml" do
  source "solr.xml"
  mode 0644
  owner 'tomcat6'
  group 'tomcat6'
end

SYSTEM_SERVICES.each do | service |
  service service do
    service_name service
    action :start
  end
end