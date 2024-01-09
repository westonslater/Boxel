import hou
from PySide2 import QtCore, QtWidgets

class Project(QtWidgets.QWidget):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance:
            cls._instance.deleteLater()  # Delete the existing instance
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, project_name, task_mode, department, task, task_version, sequence, scene, shot, work_id, work_path):
        QtWidgets.QWidget.__init__(self, hou.ui.mainQtWindow())  # Set the main Houdini window as the parent
        if hasattr(self, 'initialized'):
            return
        self.initialized = True
        self.project_name = project_name
        self.task_mode = task_mode
        self.department = department
        self.task = task
        self.task_version = task_version
        self.sequence = sequence
        self.scene = scene
        self.shot = shot
        self.work_id = work_id
        self.work_path = work_path

        self.show_initialzation_dialog()  # Call the show_initialzation_dialog method when the class is created

    def show_initialzation_dialog(self):
        QtWidgets.QMessageBox.information(self, 'Dialog', 'Task Module Activated')

    def show_current_task(self):
        message = f"Project Name: {self.project_name}\n" \
                  f"Task Mode: {self.task_mode}\n" \
                  f"Department: {self.department}\n" \
                  f"Task: {self.task}\n" \
                  f"Task Version: {self.task_version}\n" \
                  f"Sequence: {self.sequence}\n" \
                  f"Scene: {self.scene}\n" \
                  f"Shot: {self.shot}\n" \
                  f"Work ID: {self.work_id}\n" \
                  f"Work Path: {self.work_path}"
        QtWidgets.QMessageBox.information(self, 'Dialog', message)

    def handle_updated_project_data(self):
        # Add your logic here to handle the updated project data
        pass

    def closeEvent(self, event):
        self.setParent(None)  # Unparent the dialog from the main window
        event.accept()

def register_to_houdini_global_session():
    project = Project('DND', 'Sequence', 'FX', 'FireBreath', 'v001', '100', '001', '070', 'DND_100_001_070', 'H:/DND/work/sequences/100/DND_100_001/DND_100_001_070')
    setattr(hou.session, 'project', project)

register_to_houdini_global_session()
