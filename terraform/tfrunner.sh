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
#        AUTHOR:  Elvin Smith
#       VERSION:  1.0
#       CREATED:  09/21/2020
#      REVISION:  ---
#===============================================================================

if [ "$#" -ne 3 ]; then
    echo "You must enter three (3) command line arguments"
    echo "Usage: $0 staging/production aws ec2"
    exit 1
fi

echo ""
echo "------------------------------------------------------------------------"
echo "Terraform: Deploying to the ${1} environment"
echo "------------------------------------------------------------------------"
echo ""

# Go into the correct directory based on the command line parameter(s)
cd $(dirname "$0")/$1/$2/$3

# Initialize the Terraform modules
terraform init

# Generate the plan file that will be used duing the system creation
terraform plan -out=$1.tfplan

# Apply the terraform changes
terraform apply -auto-approve "${1}.tfplan"

echo ""
echo "------------------------------------------------------------------------"
echo "Terraform: Deployment to the ${1} environment completed. Exit."
echo "------------------------------------------------------------------------"
echo ""



exit 0
