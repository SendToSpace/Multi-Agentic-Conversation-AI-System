from email import contentmanager
from sys import api_version
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1
from google import genai
from google.genai.types import HttpOptions

# Replace the `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` values
# with appropriate values for your project.

# TODO(developer): Create a processor of type "OCR_PROCESSOR".

# TODO(developer): Update and uncomment these variables before running the sample.
project_id = "jmyscaner"

# Processor ID as hexadecimal characters.
# Not to be confused with the Processor Display Name.
processor_id = "fd099ee94b1bd52e"

# Processor location. For example: "us" or "eu".
location = "us"

# Path for file to process.
#To-Do(developer): the input file will sourced from the frontend.
# The file must be in one of the following formats: PDF, TIFF, GIF, PNG, JPEG, BMP, WEBP.
file_path = "C:/Users/Jie/Desktop/Recipe/backend/testingReceipt.webp"

# Set `api_endpoint` if you use a location other than "us".
opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

# Initialize Document AI client.
client = documentai_v1.DocumentProcessorServiceClient(client_options=opts)

# Get the Fully-qualified Processor path.
full_processor_name = client.processor_path(project_id, location, processor_id)

# Get a Processor reference.
request = documentai_v1.GetProcessorRequest(name=full_processor_name)
processor = client.get_processor(request=request)

# `processor.name` is the full resource name of the processor.
# For example: `projects/{project_id}/locations/{location}/processors/{processor_id}`
print(f"Processor Name: {processor.name}")

# Read the file into memory.
with open(file_path, "rb") as image:
    image_content = image.read()

# Load binary data.
# For supported MIME types, refer to https://cloud.google.com/document-ai/docs/file-types
raw_document = documentai_v1.RawDocument(
    content=image_content,
    mime_type="image/webp",
)

# Send a request and get the processed document.
request = documentai_v1.ProcessRequest(name=processor.name, raw_document=raw_document)
result = client.process_document(request=request)
document = result.document

# Read the text recognition output from the processor.
# For a full list of `Document` object attributes, reference this page:
# https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
print("The document contains the following text:")
print(document.text)

client = genai.Client(vertexai=True,project='jmyscaner',location='us-central1',http_options=HttpOptions(api_version='v1'))
response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents=(
    "You are a data extraction AI. "
    "Extract only itemized entries from the text below. "
    "Each entry must have: name (string), quantity (number), unitPrice (number), total (number). "
    "Respond ONLY with a JSON array, NO markdown, NO ```json, NO explanations. "
    "If no items are found, return an empty array []. "
    "Text to process: "
    f"{document.text}"
    )
)

print(response.text)

