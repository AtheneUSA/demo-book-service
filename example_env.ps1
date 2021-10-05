#
# Sample configuration using environment variables.
#
# The complete list of config options and associated environment variables
# is located at:
#
#   https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html
#

$env:ELASTIC_APM_ENABLED = "true"  # (true|false)
$env:ELASTIC_APM_ENVIRONMENT = "demo"  # Usually one of: (dev|qa|stage|prod)
$env:ELASTIC_APM_LOG_LEVEL = "info"  # One of: (off|critical|error|warning|info|debug|trace)
$env:ELASTIC_APM_RECORDING = "true"  # (true|false)
$env:ELASTIC_APM_SERVER_URL = "https://elk.onintranet.com:8200"
<<<<<<< HEAD
<<<<<<< HEAD
$env:ELASTIC_APM_SERVICE_NAME = "book-service-$($($(whoami) -Split '\\')[-1])"
=======
$env:ELASTIC_APM_SERVICE_NAME = "demo-book-service-$($($(whoami) -Split '\\')[-1])"
>>>>>>> 8720c01 (add sample environment variables for Windows deploy)
=======
$env:ELASTIC_APM_SERVICE_NAME = "book-service-$($($(whoami) -Split '\\')[-1])"
>>>>>>> 2b28d80 (update service name)
$env:ELASTIC_APM_VERIFY_SERVER_CERT = "False"  # (True|False)
