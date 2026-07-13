pipeline {

    agent any

    environment {
        FRONTEND_IMAGE = "aasthakumarii/frontend-service"
        CATALOG_IMAGE  = "aasthakumarii/catalog-service"
        ORDER_IMAGE    = "aasthakumarii/order-service"
        IMAGE_TAG = "latest"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Frontend') {
            steps {
                dir('Frontend_Server') {
                    sh 'docker build -t $FRONTEND_IMAGE:$IMAGE_TAG .'
                }
            }
        }

        stage('Build Catalog') {
            steps {
                dir('Catalog_Server') {
                    sh 'docker build -t $CATALOG_IMAGE:$IMAGE_TAG .'
                }
            }
        }

        stage('Build Order') {
            steps {
                dir('Order_Server') {
                    sh 'docker build -t $ORDER_IMAGE:$IMAGE_TAG .'
                }
            }
        }

        stage('Show Images') {
            steps {
                sh 'docker images | grep aasthakumarii'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }
        stage('Push Frontend') {
            steps {
                sh 'docker push $FRONTEND_IMAGE:$IMAGE_TAG'
            }
        }

        stage('Push Catalog') {
            steps {
                sh 'docker push $CATALOG_IMAGE:$IMAGE_TAG'
            }
        }

        stage('Push Order') {
            steps {
                sh 'docker push $ORDER_IMAGE:$IMAGE_TAG'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                dir('helm/bazar') {
                    sh '''
                        helm upgrade --install bazar . \
                        --namespace default
                    '''
                }
            }
        }
    }
}