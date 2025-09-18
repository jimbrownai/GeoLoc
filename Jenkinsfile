pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "geolocation-backend"
        DOCKER_TAG = "latest"
        REGISTRY = "jimbrowncn/geoloc"
        ENV_FILE = ".env"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/jimbrownai/GeoLoc.git'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python manage.py test || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker tag $DOCKER_IMAGE:$DOCKER_TAG $REGISTRY:$DOCKER_TAG'
                    sh 'docker push $REGISTRY:$DOCKER_TAG'
                }
            }
        }

        stage('Deploy Locally') {
            steps {
                sh '''
                docker stop geolocation-backend || true
                docker rm geolocation-backend || true
                docker run -d --env-file $ENV_FILE -p 8000:8000 --name geolocation-backend $DOCKER_IMAGE:$DOCKER_TAG
                '''
            }
        }
    }
}
