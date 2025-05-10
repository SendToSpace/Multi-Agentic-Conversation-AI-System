from email import contentmanager
from math import e
import re
from sys import api_version
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1
from google import genai
from google.genai.types import HttpOptions

from dotenv import load_dotenv
import os
import json

##TO-DO - add error handling for the case when the file is not found or the file is not in the correct format
## TO-DO - Upstream document AI text is not sufficient for downstream AI to extract the data. what are the options?



load_dotenv()   #load the environment variables from .env file
#setup the environment variables                                                        


#setup the project id, processor id, location and file path
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
processor_id = os.getenv("DOCUMENT_PROCESSOR_ID")
location = os.getenv("GOOGLE_CLOUD_LOCATION")
# The file must be in one of the following formats: PDF, TIFF, GIF, PNG, JPEG, BMP, WEBP.
vertex_location = os.getenv("VERTEX_LOCATION")

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
def process_img(client=client, processor=processor, file_path=None):
    # Read the file into memory.
    if not file_path:
        raise ValueError("File path is required")
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
    

    #To do:
      #use json schema supported by document ai for consistent output
    client = genai.Client(vertexai=True,project=project_id,location=vertex_location,http_options=HttpOptions(api_version='v1'))
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=(
        "You are a data extraction AI. "
        "Extract only itemized entries from the text below. "
        "Each entry must have: name (string), quantity (number), unitPrice (number), total (number). "
        "Respond ONLY with a JSON array, NO markdown, NO ```json, NO explanations. "
        "If no items are found, return an empty array []. "
        "Text to process: "
        "The documeent is a receipt. "
        "it might contain discounts, treat the discount as a negative number. similar to regular items, and name it discount. "
        f"{document.text}"
        )
    )
    return response.text

#return json object from string that contains json object structure with padded text
def filter_json(json_str):
    if not json_str:
        raise ValueError("Empty response from Document AI")
    try:
           # Remove any non-JSON content
        json_match = re.search(r'\[\s*{.*?}\s*\]', json_str, re.DOTALL)
        # Parse the JSON string to ensure it's valid
        json_obj = json.loads(json_match.group(0))
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")

    return json_obj



# Function to extract the text from the document and return the json object
def extract_text_from_document(file_path, client=client, processor=processor):
    # Process the image and get the response
    response = process_img(client, processor, file_path)
    # Filter the JSON from the response
    json_obj = filter_json(response)
    return json_obj

