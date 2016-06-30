import json, os, shutil, re, sys, urllib

__RFC_INDEX_URL__ = "https://www.rfc-editor.org/rfc/rfc-index.txt"
__OUTPUT_FILE__ = 'rfc.json'

__COMPLETE_REGEX__ = r"\n(\d{4})\s(?:(Not Issued)|(?:((?:[^\.]+\.(?!\s+[A-Z]\.))*[^\.]+)\.\s*((?:(?:[A-Z]\.)+\s*[^\.,]+(?:\.|,)\s*){1,3})(\w+\s*\d{4})\.\s*(?:\((Format[^\)]*)\))?\s*(?:\((Obsoletes[^\)]*)\))?\s*(?:\((Obsoleted\s*by[^\)]*)\))?\s*(?:\((Updates[^\)]*)\))?\s*(?:\((Updated\s*by[^\)]*)\))?\s*(?:\((Also[^\)]*)\))?\s*(?:\((Status[^\)]*)\))?\s*(?:\((DOI[^\)]*)\))?))"
__FORMAT_REGEX__   = r"Format:?\s*(.*)"
__ALSO_FYI_REGEX__ = r"Also:?\s*(.*)"
__STATUS_REGEX__   = r"Status:?\s*(.*)"
__DOI_REGEX__      = r"DOI:?\s*(.*)"
__AUTHORS_REGEX__  = r"(?:((?:[A-Z]\.)+\s[^,\.]*)[,\.]\s?)+?"
__RFC_REGEX__      = r"\s?(?:([A-Z0-9]{4,})(?:,\s)?)+?"


def create_json( rfc_index_text ):
  json_obj = {}
  matches = re.findall(__COMPLETE_REGEX__, rfc_index_text)
  for match in matches:
    rfc_number = match[0]
    if re.search("Not Issued", match[1]):
      json_obj[rfc_number] = "Not Issued"
    else:
      json_sub_obj = {}
      json_sub_obj["title"]      = clean_text(match[2])
      json_sub_obj["authors"]    = re.findall(__AUTHORS_REGEX__, clean_text(match[3]))
      month, year = clean_text(match[4]).split(" ");
      json_sub_obj["issue_data"] = {
        "month": month,
        "year": year
      }
      if match[5]!="":  json_sub_obj["format"]       = re.findall(__FORMAT_REGEX__,   clean_text(match[5]))[0]
      if match[6]!="":  json_sub_obj["obsolets"]     = re.findall(__RFC_REGEX__,      clean_text(match[6]))     #list of rfc
      if match[7]!="":  json_sub_obj["obsoleted_by"] = re.findall(__RFC_REGEX__,      clean_text(match[7]))     #list of rfc
      if match[8]!="":  json_sub_obj["updates"]      = re.findall(__RFC_REGEX__,      clean_text(match[8]))     #list of rfc
      if match[9]!="":  json_sub_obj["updated_by"]   = re.findall(__RFC_REGEX__,      clean_text(match[9]))     #list of rfc
      if match[10]!="": json_sub_obj["also_fyi"]     = re.findall(__ALSO_FYI_REGEX__, clean_text(match[10]))[0]
      if match[11]!="": json_sub_obj["status"]       = re.findall(__STATUS_REGEX__,   clean_text(match[11]))[0]
      if match[12]!="": json_sub_obj["doi"]          = re.findall(__DOI_REGEX__,      clean_text(match[12]))[0]
      json_obj[rfc_number] = json_sub_obj
  return json_obj


def clean_text(text):
  return re.sub('\s+', ' ', text).strip()


def main():
  print("Read RFC Index")
  rfc_index_text = urllib.urlopen(__RFC_INDEX_URL__).read()
  print("Done")
  output_path = __OUTPUT_FILE__
  if len(sys.argv)>=2:
    output_path = sys.argv[1]
  json_obj = create_json(rfc_index_text)
  print("Write output file")
  with open(output_path, 'w') as outfile:
    json.dump(json_obj, outfile)
  print("Done")


if __name__ == "__main__":
  print("Start Program")
  main()
  print("End Program")