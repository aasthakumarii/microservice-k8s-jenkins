pipeline {

    agent any

    environment {
        FRONTEND_IMAGE = "aasthakumarii/frontend-service"
        CATALOG_IMAGE  = "aasthakumarii/catalog-service"
        ORDER_IMAGE    = "aasthakumarii/order-service"
        IMAGE_TAG = "${BUILD_NUMBER}"
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

        stage('Update Helm Values') {
            steps {
                sh '''
                sed -i "s|frontend-service:.*|frontend-service:${IMAGE_TAG}|" helm/bazar/values.yaml
                sed -i "s|catalog-service:.*|catalog-service:${IMAGE_TAG}|" helm/bazar/values.yaml
                sed -i "s|order-service:.*|order-service:${IMAGE_TAG}|" helm/bazar/values.yaml
                '''
            }
        }

        stage('Show Updated Helm Values') {
            steps {
                sh 'cat helm/bazar/values.yaml'
            }
        }
        stage('Update Helm Chart') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {

                    sh '''
                        git config user.name "Jenkins"
                        git config user.email "jenkins@local"

                        sed -i "s|image: aasthakumarii/frontend-service:.*|image: aasthakumarii/frontend-service:${BUILD_NUMBER}|" helm/bazar/values.yaml
                        sed -i "s|image: aasthakumarii/catalog-service:.*|image: aasthakumarii/catalog-service:${BUILD_NUMBER}|" helm/bazar/values.yaml
                        sed -i "s|image: aasthakumarii/order-service:.*|image: aasthakumarii/order-service:${BUILD_NUMBER}|" helm/bazar/values.yaml

                        git add helm/bazar/values.yaml

                        git commit -m "Update image tag to ${BUILD_NUMBER}" || true

                        git push https://${GIT_USER}:${GIT_PASS}@github.com/aasthakumarii/microservice-k8s-jenkins.git HEAD:main
                    '''
                }
            }
        }
    }
}