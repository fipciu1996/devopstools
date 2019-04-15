# Devopstools
My Swiss Army knife for DevOps

During my work as DevOps Engineer I started using python for simplifying and automatic system administration or monitoring systems.
Maybe it will be also useful for someone else ;)

## Zabbix_problem_notify

There is possibility to use integrated solutions for sending SMS notifications throught Zabbix, but if for some reasons you cannot use that. This script can be great for you. After a little bit of customization you are able to run it in backgroud and it will listen for problems in Zabbix and send you SMS with AWS service SNS.
What you only need is boto3 and zabbix_api packages.

`pip install boto3`

`pip install zabbix_api`
