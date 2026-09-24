import zipfile
import os

def build_submission_zips():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Comprehensive submission package (Includes optimized Parquet data cache, ~8.4 MB)
    full_zip_path = os.path.join(base_dir, 'IBM_Project_Submission.zip')
    with zipfile.ZipFile(full_zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in ['project.py', 'requirements.txt', 'README.md', 'LICENSE']:
            p = os.path.join(base_dir, f)
            if os.path.exists(p):
                z.write(p, f)
                
        for f in ['Project_Report.pdf', 'Project_Report.docx', 'Project_Requirements.pdf', 'Project_Requirements.docx']:
            p = os.path.join(base_dir, 'reports', f)
            if os.path.exists(p):
                z.write(p, os.path.join('reports', f))
                
        for f in [
            '01_executive_overview.png',
            '02_sales_intelligence.png',
            '03_product_intelligence.png',
            '04_customer_intelligence.png',
            '05_risk_opportunity.png',
            '06_predictive_simulator.png'
        ]:
            p = os.path.join(base_dir, 'screenshots', f)
            if os.path.exists(p):
                z.write(p, os.path.join('screenshots', f))
                
        for f in ['online_retail.parquet', 'README.md']:
            p = os.path.join(base_dir, 'data', f)
            if os.path.exists(p):
                z.write(p, os.path.join('data', f))

    size_full = os.path.getsize(full_zip_path)
    print(f"Created: {full_zip_path}")
    print(f"Size: {size_full:,} bytes ({size_full/(1024*1024):.2f} MiB / {size_full/1000000:.2f} MB)")
    
    # 2. Lightweight submission package (Without parquet dataset, ~2.8 MB)
    light_zip_path = os.path.join(base_dir, 'IBM_Project_Submission_Lightweight.zip')
    with zipfile.ZipFile(light_zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in ['project.py', 'requirements.txt', 'README.md', 'LICENSE']:
            p = os.path.join(base_dir, f)
            if os.path.exists(p):
                z.write(p, f)
                
        for f in ['Project_Report.pdf', 'Project_Report.docx', 'Project_Requirements.pdf', 'Project_Requirements.docx']:
            p = os.path.join(base_dir, 'reports', f)
            if os.path.exists(p):
                z.write(p, os.path.join('reports', f))
                
        for f in [
            '01_executive_overview.png',
            '02_sales_intelligence.png',
            '03_product_intelligence.png',
            '04_customer_intelligence.png',
            '05_risk_opportunity.png',
            '06_predictive_simulator.png'
        ]:
            p = os.path.join(base_dir, 'screenshots', f)
            if os.path.exists(p):
                z.write(p, os.path.join('screenshots', f))
                
        p = os.path.join(base_dir, 'data', 'README.md')
        if os.path.exists(p):
            z.write(p, os.path.join('data', 'README.md'))

    size_light = os.path.getsize(light_zip_path)
    print(f"Created: {light_zip_path}")
    print(f"Size: {size_light:,} bytes ({size_light/(1024*1024):.2f} MiB / {size_light/1000000:.2f} MB)")

if __name__ == '__main__':
    build_submission_zips()
