pipeline {

    agent any

    environment {
        FRONTEND_IMAGE = "aasthakumarii/frontend-service"
        CATALOG_IMAGE  = "aasthakumarii/catalog-service"
        ORDER_IMAGE    = "aasthakumarii/order-service"
        IMAGE_TAG = "1.${BUILD_NUMBER}"
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
    }
}