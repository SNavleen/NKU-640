#!/bin/bash
# AWS EC2 Deployment Script for TODO REST API with uv

set -e  # Exit on error

echo "=========================================="
echo "  TODO REST API - AWS EC2 Deployment"
echo "=========================================="
echo

# Configuration
KEY_NAME="todo-api-key"
SECURITY_GROUP_NAME="todo-api-sg"
INSTANCE_TYPE="t3.micro"  # Free tier eligible
AMI_ID="ami-0c55b159cbfafe1f0"  # Ubuntu 22.04 LTS (us-east-1)
REGION="us-east-1"

echo "Configuration:"
echo "  Region: $REGION"
echo "  Instance Type: $INSTANCE_TYPE"
echo "  Key Name: $KEY_NAME"
echo

# Create key pair if it doesn't exist
if ! aws ec2 describe-key-pairs --key-names $KEY_NAME --region $REGION &> /dev/null; then
    echo "Creating SSH key pair..."
    aws ec2 create-key-pair \
        --key-name $KEY_NAME \
        --region $REGION \
        --query 'KeyMaterial' \
        --output text > ${KEY_NAME}.pem
    chmod 400 ${KEY_NAME}.pem
    echo "✓ Created key pair: ${KEY_NAME}.pem"
else
    echo "✓ Key pair already exists"
fi

# Create security group
if ! aws ec2 describe-security-groups --group-names $SECURITY_GROUP_NAME --region $REGION &> /dev/null; then
    echo "Creating security group..."
    SG_ID=$(aws ec2 create-security-group \
        --group-name $SECURITY_GROUP_NAME \
        --description "Security group for TODO REST API" \
        --region $REGION \
        --query 'GroupId' \
        --output text)

    # Add inbound rules
    aws ec2 authorize-security-group-ingress \
        --group-id $SG_ID \
        --protocol tcp \
        --port 22 \
        --cidr 0.0.0.0/0 \
        --region $REGION

    aws ec2 authorize-security-group-ingress \
        --group-id $SG_ID \
        --protocol tcp \
        --port 80 \
        --cidr 0.0.0.0/0 \
        --region $REGION

    aws ec2 authorize-security-group-ingress \
        --group-id $SG_ID \
        --protocol tcp \
        --port 443 \
        --cidr 0.0.0.0/0 \
        --region $REGION

    aws ec2 authorize-security-group-ingress \
        --group-id $SG_ID \
        --protocol tcp \
        --port 8000 \
        --cidr 0.0.0.0/0 \
        --region $REGION

    echo "✓ Created security group: $SG_ID"
else
    SG_ID=$(aws ec2 describe-security-groups \
        --group-names $SECURITY_GROUP_NAME \
        --region $REGION \
        --query 'SecurityGroups[0].GroupId' \
        --output text)
    echo "✓ Using existing security group: $SG_ID"
fi

# User data script for EC2 instance
read -r -d '' USER_DATA << 'EOF' || true
#!/bin/bash
set -e

# Update system
apt-get update -y
apt-get upgrade -y

# Install Docker
apt-get install -y docker.io
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Install Git
apt-get install -y git

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

echo "EC2 instance setup complete" > /home/ubuntu/setup-complete.txt
EOF

# Launch EC2 instance
echo "Launching EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ami-0e86e20dae9224db8 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-group-ids $SG_ID \
    --region $REGION \
    --user-data "$USER_DATA" \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=TODO-REST-API}]' \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "✓ Launched instance: $INSTANCE_ID"

# Wait for instance to be running
echo "Waiting for instance to start..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $REGION
echo "✓ Instance is running"

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --region $REGION \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo
echo "=========================================="
echo "  Deployment Information"
echo "=========================================="
echo
echo "Instance ID: $INSTANCE_ID"
echo "Public IP: $PUBLIC_IP"
echo "SSH Key: ${KEY_NAME}.pem"
echo
echo "SSH Command:"
echo "  ssh -i ${KEY_NAME}.pem ubuntu@$PUBLIC_IP"
echo
echo "Next Steps:"
echo "1. Wait 2-3 minutes for initialization"
echo "2. SSH into instance: ssh -i ${KEY_NAME}.pem ubuntu@$PUBLIC_IP"
echo "3. Clone repository or upload code"
echo "4. Run: cd python-version && docker-compose up -d"
echo "5. Access API at: http://$PUBLIC_IP:8000"
echo
echo "=========================================="

# Save deployment info
cat > deployment-info.txt <<EOL
Deployment Date: $(date)
Instance ID: $INSTANCE_ID
Public IP: $PUBLIC_IP
Region: $REGION
Key File: ${KEY_NAME}.pem

SSH Command:
ssh -i ${KEY_NAME}.pem ubuntu@$PUBLIC_IP

API URL:
http://$PUBLIC_IP:8000

Cleanup Command:
bash scripts/cleanup-aws.sh
EOL

echo "✓ Deployment info saved to: deployment-info.txt"
echo
echo "Waiting 90 seconds for instance initialization..."
sleep 90

echo
echo "Testing SSH connection..."
if ssh -i ${KEY_NAME}.pem -o StrictHostKeyChecking=no ubuntu@$PUBLIC_IP "echo 'SSH connection successful'" 2>/dev/null; then
    echo "✓ SSH connection working"
else
    echo "⚠ SSH not ready yet - wait a bit longer then try: ssh -i ${KEY_NAME}.pem ubuntu@$PUBLIC_IP"
fi

echo
echo "=========================================="
echo "  Deployment Complete!"
echo "=========================================="
