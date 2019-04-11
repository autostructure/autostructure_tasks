require 'yaml/store'
require 'fileutils'

# This fact returns a hash based on the age of the agents SSL certificate
Facter.add('auto_certificate_age') do
  setcode do
    facter_dir = Facter.value(:puppet_confdir).split('/')[0..-3].join('/') + '/facter/facts.d'
    unless File.exist?("#{facter_dir}/birthday.yaml")
      creation_time = File.ctime("#{Facter.value(:puppet_ssldir)}/certs/#{Facter.value(:fqdn)}.pem")
      time_hash = {
        year: creation_time.year,
        month: creation_time.month,
        day: creation_time.day,
      }
      FileUtils.mkdir_p facter_dir unless File.exist?(facter_dir)
      fact_file = YAML::Store.new("#{facter_dir}/birthday.yaml")
      fact_file.transaction do
        fact_file['auto_certificate_age'] = time_hash
      end
    end
  end
end
