
pipeline {
    agent any

    environment {
        GIT_REPO = 'https://github.com/Bhavyanshjain2304/MentorMind'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: "${env.GIT_REPO}", branch: 'main'
            }
        }

        stage('Verify Docker Installation') {
            steps {
                bat 'docker --version'
                bat 'docker-compose --version'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t mentor-mind .'
            }
        }

        stage('Run Docker Compose') {
            steps {
                bat 'docker-compose down'
                bat 'docker-compose up -d --build'
            }
        }
    }

    post {
        failure {
            echo '❌ Build failed!'
        }
        success {
            echo '✅ Deployment successful!'
        }
    }
}
