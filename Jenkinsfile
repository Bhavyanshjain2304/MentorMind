pipeline {
    agent {
        docker {
            image 'jenkins/jenkins:lts'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    environment {
        DOCKER_USERNAME = credentials('bhavyanshjain')
        DOCKER_PASSWORD = credentials('docker12aAA12@')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                bat '''
                    @echo off
                    REM Install Python and pip
                    powershell -Command "& {Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))}"
                    choco install python3 -y
                    choco install docker-desktop -y
                    
                    REM Install Python dependencies
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                    python -m pip install pytest pytest-cov
                '''
            }
        }
        
        stage('Test') {
            steps {
                bat '''
                    @echo off
                    set PYTHONPATH=%PYTHONPATH%;%CD%
                    python -m pytest tests/
                '''
            }
        }
        
        stage('Build Docker Images') {
            steps {
                bat '''
                    @echo off
                    docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD%
                    docker build -t %DOCKER_USERNAME%/mentormind:latest .
                    docker push %DOCKER_USERNAME%/mentormind:latest
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                bat '''
                    @echo off
                    docker-compose down
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