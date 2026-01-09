import os
import shutil
import zipfile
import subprocess


def main():
    print("Creating Lambda deployment package...")

    # Clean up
    if os.path.exists("lambda-package"):
        shutil.rmtree("lambda-package")
    if os.path.exists("lambda-deployment.zip"):
        os.remove("lambda-deployment.zip")

    # Create package directory
    os.makedirs("lambda-package")

    # Install dependencies using Docker with Lambda runtime image
    print("Installing dependencies for Lambda runtime...")

    # Use the official AWS Lambda Python 3.12 image
    # This ensures compatibility with Lambda's runtime environment
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}:/var/task",
            "--platform",
            "linux/amd64",  # Force x86_64 architecture
            "--entrypoint",
            "",  # Override the default entrypoint
            "public.ecr.aws/lambda/python:3.12",
            "/bin/sh",
            "-c",
            "pip install --target /var/task/lambda-package -r /var/task/requirements.txt --platform manylinux2014_x86_64 --only-binary=:all: --upgrade",
        ],
        check=True,
    )
    # --- 🧹 KRİTİK TEMİZLİK ADIMI ---
    print("🧹 Gereksiz kütüphaneler (Lambda'da zaten var olanlar) temizleniyor...")
    
    # Bu kütüphaneler AWS Lambda Python Runtime içinde zaten var.
    # Paketine dahil etmene gerek yok, yer kaplamasınlar.
    libs_to_remove = ["boto3", "botocore", "s3transfer", "jmespath"]
    
    package_dir = "lambda-package"
    
    for item in os.listdir(package_dir):
        # Klasör/Dosya adı listemizdekilerden biriyle başlıyorsa sil
        for lib in libs_to_remove:
            if item == lib or item.startswith(f"{lib}-"):
                full_path = os.path.join(package_dir, item)
                if os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                    print(f"   🗑️  Silindi: {item}")
                elif os.path.isfile(full_path):
                    os.remove(full_path)
                    print(f"   🗑️  Silindi: {item}")
    # -------------------------------

    # Copy application files
    print("Copying application files...")
    for file in ["server.py", "lambda_handler.py", "context.py", "resources.py"]:
        if os.path.exists(file):
            shutil.copy2(file, "lambda-package/")

    # Copy data directory
    if os.path.exists("data"):
        shutil.copytree("data", "lambda-package/data")

    # Create zip
    print("Creating zip file...")
    with zipfile.ZipFile("lambda-deployment.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("lambda-package"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "lambda-package")
                zipf.write(file_path, arcname)

    # Show package size
    size_mb = os.path.getsize("lambda-deployment.zip") / (1024 * 1024)
    print(f"✓ Created lambda-deployment.zip ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
