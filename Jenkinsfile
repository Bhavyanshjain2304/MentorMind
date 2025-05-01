pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Bhavyanshjain2304/MentorMind.git',
                        credentialsId: ''
                    ]],
                    extensions: [[
                        $class: 'CloneOption',
                        depth: 1,
                        noTags: true,
                        shallow: true
                    ]]
                ])
            }
        }
        
        stage('Build') {
            steps {
                bat '''
                    @echo off
                    echo Building the application...
                    python -m pip install -r requirements.txt
                '''
            }
        }
        
        stage('Test') {
            steps {
                bat '''
                    @echo off
                    echo Running tests...
                    python -m pytest tests/
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                bat '''
                    @echo off
                    echo Deploying the application...
                    docker-compose up -d --build
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}