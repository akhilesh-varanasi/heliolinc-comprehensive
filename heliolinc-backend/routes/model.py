from fastapi import APIRouter, Request, BackgroundTasks, Query, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from routes.run_heliolinc import run_heliolinc
from routes.ades import read_psv_ades
from routes.postgres import preprocess_csv
import uuid
import os
import time
import zipfile
import stat
from concurrent.futures import ThreadPoolExecutor
import asyncio

router = APIRouter(
    prefix="/model",
    tags=["model"],
    responses={
        404: {"description" : "Not found"}
    },
)

html_directory = "/astro/store/epyc/users/avaran/public_html/"
zip_directory = "/astro/store/epyc/users/avaran/zip_files/"

@router.post("/generate")
async def generate(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    # Save the file
    print(os.getcwd())
    file_location = f"temp_files/{uid}_input.csv"
    with open(file_location, "wb") as file_out:
        file_out.write(await file.read())
    print("hello")
    # df, header = read_psv_ades(file_location)
    # print(df.columns)
    print("start")
    await preprocess_csv(file_location)
    print("done")
    # create_temporary_landing_page(uid)
    # background_tasks.add_task(run_heliolinc_background, uid, background_tasks)
    return {"uuid": uid}

def create_temporary_landing_page(uid: str):
    temp_content = f"""
    <html>
        <head>
            <title>Processing Your Request</title>
            <meta http-equiv="refresh" content="10">
        </head>
        <body>
            <h1>Your request (id: {uid}) is being processed</h1>
            <p>Please wait on this page. This page will automatically update when your file is ready to download.</p>
        </body>
    </html>
    """
    landing_page_path = os.path.join(html_directory, f"{uid}.html")
    print(landing_page_path)
    with open(landing_page_path, 'w') as file:
        file.write(temp_content)

def replace_with_download_page(uid: str, file_name: str):
    # The download link is now a button that will trigger a JavaScript function.
    download_button_html = f"""
    <button id="downloadButton" onclick="downloadFile()">Download File</button>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script>
        function downloadFile() {{
            axios({{
                url: 'http://localhost:8332/api/model/download?uid={uid}',
                method: 'GET',
                responseType: 'blob', // This is important
            }})
            .then((response) => {{
                // Handle the success response, initiate a download
                const url = window.URL.createObjectURL(new Blob([response.data], {{ type: 'application/zip' }}));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', '{file_name}'); 
                document.body.appendChild(link);
                link.click();
                window.URL.revokeObjectURL(url); // Clean up the URL object
                document.body.removeChild(link);
            }})
            .catch((error) => {{
                console.error('There was an error downloading the file:', error);
            }});
        }}
    </script>
    """

    download_content = f"""
    <html>
        <head>
            <title>Your File is Ready</title>
        </head>
        <body>
            <h1>Your file is ready!</h1>
            <p>Your file has been processed and is now ready for download:</p>
            {download_button_html}
        </body>
    </html>
    """

    # Replace 'html_directory' with the actual path where you want to save the HTML file.
    landing_page_path = os.path.join(html_directory, f"{uid}.html")
    with open(landing_page_path, 'w') as file:
        file.write(download_content)
    print("replaced")



def run_heliolinc_background(uid: str, background_tasks: BackgroundTasks):
    loop = asyncio.new_event_loop()
    with ThreadPoolExecutor() as executor:
        executor.submit(loop.run_until_complete, run_heliolinc(uid))
    time.sleep(5)
    # generate zip file and create download page
    # note that we are already in the ./heliolinc2/tests dir b/c of run_heliolinc
    all_csv_path = "tracklets_test01.csv"
    summary_csv_path = "trk2det_test01_compare.csv"
    zip_file_name = f"{uid}.zip"
    zip_file_path = os.path.join(zip_directory, zip_file_name)
    # Create a zip file and add your CSV files
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(all_csv_path, arcname="all_links.csv")
        zipf.write(summary_csv_path, arcname="link_summary.csv")
    print("FILES ZIPPED")
    os.chdir(os.path.dirname(os.path.dirname(__file__))) # need to reset to main dir
    os.chmod(zip_file_path, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
    # Once the process is complete, replace the temporary page with the download page
    background_tasks.add_task(replace_with_download_page, uid, zip_file_name)

@router.get("/download")
async def download(uid: str = Query(...)):
    print("UID is", uid)
    file_path = os.path.join(zip_directory, f"{uid}.zip")
    if os.path.exists(file_path):
        print(file_path)
        return FileResponse(path=file_path, filename=f"{uid}.zip", media_type='application/zip')
    else:
        raise HTTPException(status_code=404, detail="File not found")
