pipeline {
    agent any
    stages {
        // stage('Clone') {
        //     steps {
        //         echo 'Inside Clone Stage'
        //         git branch: 'main', url: 'https://github.com/ankitr-c/db-calculator-app.git'
        //     }
        // }
        stage('Config') {
            steps {
                echo 'Inside Config Stage'
                script {
                    sh '''
                    sudo apt update
                    sudo apt install -y python3-pip
                    sudo pip3 install -r requirements.txt
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Inside Deploy Stage'
                script {
                    sh '''
                    sudo python3 schema.py
                    sudo nohup /usr/bin/python3 main.py > output.log 2>&1 &
                    '''
                }
            }
        }
    }
}
