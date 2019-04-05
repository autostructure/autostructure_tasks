# This fact returns a hash based on the age of the agents SSL certificate
Facter.add('certificate_age') do
  setcode do
    creation_time = File.birthtime("#{Facter.value(:puppet_ssldir)}/certs/#{Facter.value(:fqdn)}.pem")
    # Return a hash { day: x, month: x, year: x }
    time_hash = {
      year: creation_time.year,
      month: creation_time.month,
      day: creation_time.day,
    }
    time_hash
  end
end
