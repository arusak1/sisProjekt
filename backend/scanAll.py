from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import yaml

app = Flask(__name__)
CORS(app)

def get_clusters_from_kubeconfig(kubeconfig_path):
    with open(kubeconfig_path, 'r') as file:
        kubeconfig = yaml.safe_load(file)

    clusters = []
    for context in kubeconfig.get('contexts', []):
        cluster_name = context['context']['cluster']
        clusters.append(cluster_name)

    return clusters

def scan_kubernetes_clusters(kubeconfig_path, output_file_path):
    try:
        clusters = get_clusters_from_kubeconfig(kubeconfig_path)

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for cluster in clusters:
                command = f"trivy k8s all --report all cluster --kubeconfig {kubeconfig_path} --context {cluster}"
                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=False)

                result_stdout = result.stdout.decode('utf-8').strip() if result.stdout else ""

                output_file.write(f"Scan result for cluster '{cluster}' in kubeconfig: {kubeconfig_path}\n")
                output_file.write(result_stdout)
                output_file.write("\n")

    except subprocess.CalledProcessError as e:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            error_message = f"Error scanning cluster in kubeconfig: {kubeconfig_path}\n"
            error_message += f"Error message: {e.stderr.decode('utf-8')}\n"
            output_file.write(error_message)

@app.route('/api/scanAll', methods=['GET'])
def start_scan_all():
    kubeconfig_path = r"C:\Users\Rule\.kube\config"
    output_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "scanAll_results.txt")

    scan_kubernetes_clusters(kubeconfig_path, output_file_path)

    with open(output_file_path, 'r', encoding='utf-8') as result_file:
        scan_result = result_file.read()

    response = jsonify({'scanAll_result': scan_result})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)
