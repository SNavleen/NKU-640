#!/bin/bash
# AWS Cleanup Script - Remove all created resources

set -e

echo "=========================================="
echo "  AWS Resource Cleanup"
echo "=========================================="
echo

# Configuration
KEY_NAME="todo-api-key"
SECURITY_GROUP_NAME="todo-api-sg"
REGION="us-east-1"

# Warning
echo "WARNING: This will delete:"
echo "  - EC2 instances tagged 'TODO-REST-API'"
echo "  - Security group: $SECURITY_GROUP_NAME"
echo "  - Key pair: $KEY_NAME"
echo
read -p "Are you sure? (yes/no): " -r
if [[ ! $REPLY == "yes" ]]; then
    echo "Cancelled"
    exit 0
fi

# Find and terminate instances
echo "Finding instances..."
INSTANCE_IDS=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=TODO-REST-API" "Name=instance-state-name,Values=running,stopped" \
    --region $REGION \
    --query 'Reservations[*].Instances[*].InstanceId' \
    --output text)

if [ -n "$INSTANCE_IDS" ]; then
    echo "Terminating instances: $INSTANCE_IDS"
    aws ec2 terminate-instances --instance-ids $INSTANCE_IDS --region $REGION
    echo "Waiting for instances to terminate..."
    aws ec2 wait instance-terminated --instance-ids $INSTANCE_IDS --region $REGION
    echo "✓ Instances terminated"
else
    echo "✓ No instances to terminate"
fi

# Delete security group
if aws ec2 describe-security-groups --group-names $SECURITY_GROUP_NAME --region $REGION &> /dev/null; then
    echo "Deleting security group..."
    aws ec2 delete-security-group --group-name $SECURITY_GROUP_NAME --region $REGION
    echo "✓ Security group deleted"
else
    echo "✓ Security group already deleted"
fi

# Delete key pair
if aws ec2 describe-key-pairs --key-names $KEY_NAME --region $REGION &> /dev/null; then
    echo "Deleting key pair..."
    aws ec2 delete-key-pair --key-name $KEY_NAME --region $REGION
    echo "✓ Key pair deleted"

    # Remove local key file
    if [ -f "${KEY_NAME}.pem" ]; then
        rm "${KEY_NAME}.pem"
        echo "✓ Local key file removed"
    fi
else
    echo "✓ Key pair already deleted"
fi

# Remove deployment info
if [ -f "deployment-info.txt" ]; then
    rm deployment-info.txt
    echo "✓ Deployment info removed"
fi

echo
echo "=========================================="
echo "  Cleanup Complete"
echo "=========================================="
echo
echo "All AWS resources have been removed."
