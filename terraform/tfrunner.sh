#! /bin/bash
#===============================================================================
#
#          FILE:  tfrunner.sh
#
#         USAGE:  tfrunner.sh [ENVIRONMENT] [CLOUD PROVIDER] [SERVICE]
#
#         EXAMPLE: tfrunner.sh staging aws ec2
#
#   DESCRIPTION:  Terrafrom runner script
#
#       OPTIONS:  ---
#  REQUIREMENTS:  ENVIRONMENT (staging/production)
#                 CLOUD PROVIDER (aws/gcp)
#                 SERVICE (ec2, rds, etc.)
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Elvin Smith, esmith@crisistextline.org
#       COMPANY:  Crisis Text line
#       VERSION:  1.0
#       CREATED:  09/21/2020
#      REVISION:  ---
#===============================================================================


# ---------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------

# Go into the correct directory based on the command line parameter(s)
source $(dirname "$0")/$1/$2/

# Initialize the Terraform modules
terraform init

# Generate the plan file that will be used duing the system creation
terraform plan -out=staging.tfplan

# Apply the terraform changes
terraform apply "staging.tfplan"

exit 0