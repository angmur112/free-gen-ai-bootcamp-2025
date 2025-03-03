import os
import sys

# Debug: Print current directory and Python path
print(f"Current working directory: {os.getcwd()}")
print(f"Current file location: {os.path.abspath(__file__)}")
print(f"Python path before: {sys.path}")

# Add both the current and parent directories to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

print(f"Python path after: {sys.path}")

try:
    from comps.service_orchestrator import ServiceOrchestrator
except ImportError as e:
    print(f"Detailed import error: {e}")
    print(f"Looking for module in directories: {[current_dir, parent_dir]}")
    print(f"Directory contents: {os.listdir(current_dir)}")
    if os.path.exists(os.path.join(current_dir, 'comps')):
        print(f"Contents of comps: {os.listdir(os.path.join(current_dir, 'comps'))}")
    sys.exit(1)

class Chat:
    def __init__(self):
        print('init')
        self.megaservice = ServiceOrchestrator()
        self.endpoint = '/angelo chatbot'

    def add_remote_service(self):
        print('add_remote_service')

    def start(self):
        print('start')

if __name__ == '__main__':
    print('main')
    chat = Chat()
    chat.add_remote_service()
    chat.start()
