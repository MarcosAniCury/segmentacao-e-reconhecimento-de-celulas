import os
import shutil


def setup_binary_classification_structure(root_path, src_folder, dest_folder):
    """
    Set up a binary classification directory structure and copy files from the original dataset.

    :param root_path: The base directory path.
    :param src_folder: The source folder name, where the original dataset is located.
    :param dest_folder: The destination folder name for the binary classification.
    """
    src_path = os.path.join(root_path, src_folder)
    dest_path = os.path.join(root_path, dest_folder)

    # Define the class names for binary classification
    classes = ['NEGATIVE', 'OTHERS']

    # Create the binary classification structure
    for phase in ['training', 'test']:
        for class_name in classes:
            new_class_dir = os.path.join(dest_path, phase, class_name)
            os.makedirs(new_class_dir, exist_ok=True)

    # Function to copy files into the new structure
    def copy_files(class_name, phase):
        src_class_dir = os.path.join(src_path, phase, class_name)
        dest_class_dir = os.path.join(dest_path, phase, 'NEGATIVE' if class_name == 'NEGATIVE' else 'OTHERS')

        for filename in os.listdir(src_class_dir):
            src_file = os.path.join(src_class_dir, filename)
            dest_file = os.path.join(dest_class_dir, filename)
            shutil.copy2(src_file, dest_file)

    # Copy 'NEGATIVE' class files
    for phase in ['training', 'test']:
        copy_files('NEGATIVE', phase)

    # Copy all other class files
    other_classes = [cls for cls in os.listdir(os.path.join(src_path, 'training')) if cls != 'NEGATIVE']
    for phase in ['training', 'test']:
        for class_name in other_classes:
            copy_files(class_name, phase)
