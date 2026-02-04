pipeline {
    agent any

    environment {
        // Using the same credentials ID as the Maven/NPM project
        ARTIFACTORY_CREDS = credentials('StagingPwd')
        // Update this URL with your actual Python repository name in Artifactory
        // typically .../api/pypi/<repo-key>/simple
        ARTIFACTORY_URL = "observe.fortknox.commercialstaging.dev.veedna.com/artifactory/api/pypi/gos-all-proxy-python/simple"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    // Set up the pip index URL with authentication
                    // We encode the URL to include the credentials safely in the environment
                    def pipIndexUrl = "https://${ARTIFACTORY_CREDS_USR}:${ARTIFACTORY_CREDS_PSW}@${ARTIFACTORY_URL}"
                    
                    withEnv(["PIP_INDEX_URL=${pipIndexUrl}"]) {
                         // Optional: Create a virtual environment
                        sh 'rm -rf venv'
                        sh 'python3 -m venv venv'
                        
                        // Windows typically uses venv\Scripts\activate, Linux uses . venv/bin/activate
                        // Since we are likely in a linux-like shell environment in Jenkins (even on Windows agents often), 
                        // calling the python executable in the venv directly is safer/easier.
                        
                        // Install dependencies
                        // PIP_INDEX_URL env var is automatically picked up by pip
                        sh './venv/bin/python -m pip --version'
                        // sh './venv/bin/python -m pip install --upgrade pip'
                        sh './venv/bin/python -m pip cache purge'
                        sh './venv/bin/python -m pip install -vvv --no-cache-dir --index-url "${PIP_INDEX_URL}" --trusted-host jfrog.commercialdev.dev.veedna.com -r requirements.txt'
                        
                        // Run the script
                        sh './venv/bin/python main.py'
                    }
                }
            }
        }
    }
}
