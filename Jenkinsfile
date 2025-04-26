pipeline {
    agent any
    
    environment {
        DOCKER_COMPOSE_VERSION = '1.29.2'
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Bhavyanshjain2304/MentorMind.git'
            }
        }
        
        stage('Install Docker Compose') {
            steps {
                script {
                    // Install Docker Compose if not already installed
                    sh 'curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose'
                    sh 'chmod +x /usr/local/bin/docker-compose'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image using docker-compose
                    sh 'docker-compose -f docker-compose.yml build'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Run the app using docker-compose
                    sh 'docker-compose -f docker-compose.yml up -d'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Add test steps here if needed
                    echo 'Running tests (if any)...'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deploy the container
                    echo 'Deploying application...'
                }
            }
        }
    }

    post {
        always {
            // Clean up and stop containers after build
            sh 'docker-compose -f docker-compose.yml down'
        }
    }
}
