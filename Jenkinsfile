pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = '481063092768'
        ECR_REPOSITORY = 'mindmate-main-app'
        REPOSITORY_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${ECR_REPOSITORY}"
        DOCKER_IMAGE_NAME = 'mindmate-main-app'
        
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout your Django app code from your version control system (e.g., Git)
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image of your Django app
                    dir('/home/ubuntu/.jenkins/workspace/MindMatePipeline') {

                        sh 'ls -la'  // Replace with your actual commands
                        sh 'echo "This is the workspace directory."'
                    }
                    def dockerImage = docker.build(env.DOCKER_IMAGE_NAME)

                    // Tag the Docker image for ECR repository
                    dockerImage.tag("${env.ECR_REPOSITORY}:latest")
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    // Authenticate Docker with AWS ECR using the get-login-password command
                    def ecrLoginCmd = "aws ecr get-login-password --region ${env.AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin 481063092768.dkr.ecr.us-east-1.amazonaws.com"
                    sh ecrLoginCmd

                    // Push the Docker image to ECR
                    def dockerImage = docker.image("${env.ECR_REPOSITORY}:latest")
                    dockerImage.push()
                }
            }
        }
    }

    post {
        success {
            echo 'Docker image successfully built and pushed to ECR!'
        }
        failure {
            echo 'Docker image failed to be built and pushed to ECR!'
        }
    }
}
