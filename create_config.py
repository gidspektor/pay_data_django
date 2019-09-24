import configparser
config = configparser.ConfigParser()

config['DEFAULT'] = {
  'api':'https://openpaymentsdata.cms.gov/resource/j3ph-dt9p.json'
}

with open('config.ini', 'w') as configfile:
  config.write(configfile)
