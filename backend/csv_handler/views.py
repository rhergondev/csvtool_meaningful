import os
import uuid
import tempfile
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .services import process_csv_files

TEMP_CSV_DIR = getattr(settings, "TEMP_CSV_DIR", settings.BASE_DIR / "temp_csv_files")
os.makedirs(TEMP_CSV_DIR, exist_ok=True)


@require_http_methods(["POST"])
@login_required
@csrf_protect
def upload_csv_files(request):
    """
    Handle the CSV file upload.
    """
    print("request.FILES:", request.FILES)

    file1 = request.FILES.get("file1")
    file2 = request.FILES.get("file2")

    if not file1 or not file2:
        return JsonResponse({"error": "Both files are required."}, status=400)

    if not file1.name.endswith(".csv") or not file2.name.endswith(".csv"):
        return JsonResponse({"error": "Only CSV files are allowed."}, status=400)

    try:
        processed_df = process_csv_files(file1, file2)

        unique_id = uuid.uuid4()
        temp_filename = f"processed_{unique_id}.csv"
        temp_file_path = os.path.join(TEMP_CSV_DIR, temp_filename)

        processed_df.to_csv(temp_file_path, index=False, encoding="utf-8")

        download_url = reverse(
            "csv_download_processed", kwargs={"file_id": str(unique_id)}
        )

        return JsonResponse(
            {
                "message": "Files processed successfully.",
                "download_url": download_url,
                "processed_file": temp_filename,
            },
            status=200,
        )
    except ValueError as e:
        print(f"View Error (ValueError): {e}")
        return JsonResponse({"error": str(e)}, status=400)
    except RuntimeError as e:
        print(f"View Error (RuntimeError): {e}")
        return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        print(f"View Error (unexpected): {e}")
        return JsonResponse(
            {"error": "An unexpected error occurred on the server."}, status=500
        )


@require_http_methods(["GET"])
@login_required
def download_processed_file(request, file_id):
    try:
        uuid.UUID(str(file_id))
        filename = f"processed_{file_id}.csv"
        filepath = os.path.join(TEMP_CSV_DIR, filename)

        print(f"Attemting to download file: {file_id} @ {filepath}")

        if os.path.exists(filepath):
            with open(filepath, "rb") as file:
                response = HttpResponse(file.read(), content_type="text/csv")
                response["Content-Disposition"] = f'attachment; filename="{filename}"'
                print(f"File {filename} downloaded successfully.")
                # try:
                #     os.remove(filepath)
                #     print(f"File {filename} deleted successfully.")
                # except os.error as e:
                #     print(f"Error deleting file {filename}: {e}")
                return response
        else:
            print(f"File {filename} not found.")
            raise Http404("File not found or it was allready deleted.")
    except ValueError as e:
        print(f"View Error (ValueError): {e}")
        return JsonResponse({"error": "Invalid file ID."}, status=400)
    except Exception as e:
        print(f"View Error (unexpected): {e}")
        return JsonResponse({"error": "Internal error occured"}, status=500)
