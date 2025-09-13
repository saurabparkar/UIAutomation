pipeline {
    agent any

    environment {
        VENV = ".venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Env') {
            steps {
                bat '''
                python -m venv %VENV%
                call %VENV%\\Scripts\\activate
                pip install --upgrade pip setuptools wheel
                pip install -r requirements.txt
                '''
            }
        }

        stage('Build Package') {
            steps {
                bat '''
                call %VENV%\\Scripts\\activate
                python setup.py sdist bdist_wheel
                pip install dist\\*.whl
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                call %VENV%\\Scripts\\activate
                pytest --maxfail=1 --disable-warnings -q --junitxml=reports\\results.xml
                '''
            }
        }

        stage('Archive Reports') {
            steps {
                junit 'reports\\results.xml'
                archiveArtifacts artifacts: 'reports\\**\\*.xml', fingerprint: true
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
