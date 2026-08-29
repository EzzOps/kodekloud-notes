# Enrichment Pipeline

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Implementing-an-Intelligent-Search-Solution/Enrichment-Pipeline/page

Explains Azure Cognitive Search enrichment pipeline converting raw files and images into structured searchable index documents using AI skills like language detection OCR key phrase extraction and entity recognition.

This lesson explains the enrichment pipeline in Azure Cognitive Search (AI Search): how raw files (text + images) are transformed by AI skills into structured, searchable index documents. The pipeline flow covers ingestion → AI enrichment (skills such as language detection, OCR, key-phrase extraction, entity recognition, merge) → indexing → searchable index documents.

Why this matters

* Turn unstructured content (PDFs, images, scanned docs) into searchable insights.
* Use AI skills to extract language, text from images, key phrases, and named entities.
* Support rich search experiences: full-text search, filters, facets, and entity-based queries.

Pipeline overview

The pipeline starts with document ingestion and basic extraction (metadata and any embedded text). The indexer then invokes a skillset (AI skills) to enrich the document. Outputs from the skillset are mapped into an index schema and stored for query-time usage.

<Frame>
  <img alt="A slide titled &#x22;Enrichment Pipeline&#x22; showing a central pipeline icon branching to three boxes labeled Skill 1: Language Detection, Skill 2: OCR, and Skill 3: Merge, each listing their inputs and outputs. It illustrates how document content and images are detected for language, OCR-extracted, then merged into unified structured content for indexing." />
</Frame>

Common skills and outputs

| Skill                               | Purpose                                                      | Typical output field(s)                        |
| ----------------------------------- | ------------------------------------------------------------ | ---------------------------------------------- |
| Language Detection                  | Detect document language to enable language-aware analyzers  | language: "en"                                 |
| OCR (Optical Character Recognition) | Extract text from images/pages                               | images\[i].text                                |
| Merge / MergeSkill                  | Combine original content + OCR text into a single text field | merged\_text / document\_text                  |
| Key Phrase Extraction               | Pull out salient phrases for indexing/faceting               | keyPhrases (collection)                        |
| Entity Recognition                  | Identify people, locations, organizations                    | people, locations, organizations (collections) |

Input document example

Before enrichment, documents generally arrive as JSON with metadata, a content field, and an images array. The indexer processes this JSON as the pipeline input:

```json theme={null}
{
  "metadata_source": "file_system",
  "metadata_creator": "John Doe",
  "content": "Original text extracted from the file (if any).",
  "images": [
    {
      "name": "page1.png",
      "text": null
    }
  ]
}
```

How language detection, OCR, and merge work (example)

* Language detection reads the `content` and writes a language code:
  * output: `"language": "en"`

* OCR scans each image in the `images` array and populates the `text` field per image:
  * `images[0].text = "Scanned text extracted from image"`

* The merge skill concatenates the original `content` and the OCR-extracted texts into one unified field suitable for indexing:
  * output: `"merged_text": "Full structured text including OCR-extracted data"`

After enrichment, the document becomes a structured JSON object ready for indexing:

```json theme={null}
{
  "metadata_source": "file_system",
  "metadata_creator": "John Doe",
  "content": "Original text extracted from the file (if any).",
  "images": [
    {
      "name": "page1.png",
      "text": "Scanned text extracted from image"
    }
  ],
  "language": "en",
  "merged_text": "Full structured text including OCR-extracted data"
}
```

Indexed document example

When fields are projected into an index suitable for queries, the index document typically contains metadata and the merged/document text fields that applications will query:

```json theme={null}
{
  "file_name": "contract.pdf",
  "creator": "John Doe",
  "language": "en",
  "document_text": "Full structured text including OCR-extracted data"
}
```

Walkthrough — create an AI Search pipeline in the Azure portal

This walkthrough outlines the high-level steps in the Azure portal. Screenshots below correspond to each step.

1. Store files in Azure Blob Storage\
   Example: a `resume` container containing PDF resumes (source for the indexer).

<Frame>
  <img alt="A screenshot of a cloud storage file list (folder: &#x22;resume&#x22;) showing three PDF files: Aisha_Khan_Resume.pdf, Carlos_Rivera_Resume.pdf, and John_Doe_Resume.pdf. Each file is dated 4/20/2025, 1:13:27 PM and marked with access tier &#x22;Hot (Inferred).&#x22;" />
</Frame>

2. Create an Azure Cognitive Search service\
   Deploy an Azure Cognitive Search (AI Search) resource in your subscription and open the resource.

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing a completed deployment named &#x22;searchservice-1745144148960&#x22; with a &#x22;Your deployment is complete&#x22; message and a &#x22;Go to resource&#x22; button. A &#x22;Deployment succeeded&#x22; notification is visible in the top-right." />
</Frame>

3. Add a data source that points to your Blob Storage container\
   Configure the data source to point to the container (e.g., `resume`). Optionally enable deletion detection to reflect deleted blobs in the index.

<Frame>
  <img alt="A Microsoft Azure portal &#x22;Add data source&#x22; form for Azure Blob Storage with fields filled (name &#x22;resume-datasource&#x22;, subscription &#x22;Kodekloud Labs&#x22;, storage account &#x22;azai102imagestore&#x22;). The blob container dropdown is open showing options like &#x22;images&#x22;, &#x22;resume&#x22; and &#x22;video&#x22;, and a cursor is selecting &#x22;resume&#x22;." />
</Frame>

> **lightbulb** You must connect an AI resource to enable AI enrichment skills. This can be an Azure Cognitive Services resource or Azure OpenAI. Provide that cognitive service when creating the skillset so skills like OCR, key-phrase extraction, and entity recognition run correctly.

4. Create a skillset (AI skills)

A skillset contains the set of AI skills the indexer will execute. Below is a simplified skillset JSON with a key-phrase extraction skill and an entity recognition skill. Replace the cognitive services subdomain with your resource endpoint or use key-based config.

```json theme={null}
{
  "name": "resume-skill",
  "description": "Skillset for extracting key phrases and entities from resumes",
  "skills": [
    {
      "@odata.type": "#Microsoft.Skills.Text.KeyPhraseExtractionSkill",
      "name": "key-phrase-skill",
      "description": "Extract key phrases from document content",
      "inputs": [
        {
          "name": "text",
          "source": "/document/content"
        }
      ],
      "outputs": [
        {
          "name": "keyPhrases",
          "targetName": "keyPhrases"
        }
      ],
      "defaultLanguageCode": "en",
      "maxKeyPhraseCount": 10
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.V3.EntityRecognitionSkill",
      "name": "entity-skill",
      "description": "Recognize people, locations, and organizations",
      "inputs": [
        {
          "name": "text",
          "source": "/document/content"
        }
      ],
      "outputs": [
        {
          "name": "persons",
          "targetName": "people"
        },
        {
          "name": "locations",
          "targetName": "locations"
        },
        {
          "name": "organizations",
          "targetName": "organizations"
        }
      ],
      "defaultLanguageCode": "en",
      "includeTypelessEntities": true
    }
  ],
  "cognitiveServices": {
    "subdomainUrl": "https://<your-cognitive-service>.cognitiveservices.azure.com/",
    "description": "Provide the cognitive services endpoint or use the key-based configuration"
  }
}
```

5. Create an index (define schema)

Design an index schema that includes fields produced by your skillset (e.g., keyPhrases, people, locations, organizations) and standard metadata fields. Choose analyzers and field attributes (searchable, retrievable, filterable, facetable) based on how you plan to query/filter results.

Typical fields you’ll add in the portal:

* id (key)
* metadata\_storage\_name (string; retrievable, filterable)
* metadata\_storage\_path (string; retrievable)
* document\_text (string; searchable, retrievable)
* keyPhrases (collection(string); searchable, filterable, facetable, retrievable)
* people, locations, organizations (collection(string); searchable, filterable, facetable, retrievable)

Example index JSON (simplified):

```json theme={null}
{
  "name": "resume-index",
  "fields": [
    { "name": "id", "type": "Edm.String", "key": true, "retrievable": true },
    { "name": "metadata_storage_name", "type": "Edm.String", "retrievable": true, "filterable": true },
    { "name": "metadata_storage_path", "type": "Edm.String", "retrievable": true },
    { "name": "document_text", "type": "Edm.String", "searchable": true, "retrievable": true },
    { "name": "keyPhrases", "type": "Collection(Edm.String)", "searchable": true, "filterable": true, "facetable": true, "retrievable": true },
    { "name": "people", "type": "Collection(Edm.String)", "searchable": true, "filterable": true, "facetable": true, "retrievable": true },
    { "name": "locations", "type": "Collection(Edm.String)", "searchable": true, "filterable": true, "facetable": true, "retrievable": true },
    { "name": "organizations", "type": "Collection(Edm.String)", "searchable": true, "filterable": true, "facetable": true, "retrievable": true }
  ]
}
```

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal on a Mac showing the &#x22;Create index&#x22; page. It displays an index name input and a table of fields (id, metadata_storage_name, content, keyPhrases, people, locations, organizations) with checkboxes for properties like retrievable, searchable, and facetable." />
</Frame>

6. Create an indexer (connect data source, skillset, and index)

The indexer orchestrates ingestion and enrichment: it reads from the data source, invokes the skillset, and pushes transformed documents into the index. Configure:

* Schedule (continuous or cron)
* Parsing mode (default vs. try-legacy)
* Allowed/excluded file extensions
* Batch size and retry settings
* Image action (if OCR is required)

<Frame>
  <img alt="A screenshot of the Microsoft Azure portal showing the &#x22;Add indexer&#x22; configuration page with fields for Skillset, Schedule and many advanced settings (batch size, max failed items, excluded/indexed extensions, parsing mode, image action, etc.). The page is open in a web browser on a macOS desktop with several tabs visible." />
</Frame>

7. Run the indexer and monitor results

After the indexer runs, review success counts, errors, and warnings in the portal. Once indexing is complete, open the index and run queries to inspect results.

Example search result (sample)

```json theme={null}
{
  "@search.score": 1.8703225,
  "id": "aHR0cHM6Ly9hemExMDIxaW1hZ2VzdG9yZS5ibG9iLmNvcmUud2luZG93cy5uZXQvcmVzdW1lL0Fpc2hhX0toYW5fUmVzdW1lLnBkZg==",
  "metadata_storage_name": "Aisha_Khan_Resume.pdf",
  "metadata_storage_path": "https://azai102imagestore.blob.core.windows.net/resume/Aisha_Khan_Resume.pdf",
  "document_text": "Name: Aisha Khan\nTitle: Data Scientist\nLocation: Dubai, UAE\n\nSkills: Python, Machine Learning, ...",
  "keyPhrases": [
    "Aisha Khan",
    "Data Scientist",
    "Power BI",
    "Azure ML Studio",
    "machine learning models",
    "financial forecasting",
    "Dubai",
    "Python",
    "Pandas"
  ],
  "people": [
    "Aisha Khan"
  ],
  "locations": [
    "Dubai",
    "UAE"
  ],
  "organizations": []
}
```

Search scenarios and common queries

* Full-text search: keyword queries on `document_text` return relevance-ranked matches.
* Filters & facets: narrow results by `locations`, `people`, or `keyPhrases` (e.g., filter by location = "Dubai").
* Skill-driven search: search the `keyPhrases` collection to locate candidates with specific skills like "Python" or "DevOps".

Summary and best practices

* The enrichment pipeline converts raw files (including scanned images) into structured, searchable documents by chaining AI skills (OCR, language detection, key-phrase extraction, entity recognition, merge).
* Portal sequence: create a data source → create/connect a Cognitive Services or Azure OpenAI resource → create a skillset → create an index → create an indexer → run and monitor the indexer.
* Index design matters: choose correct analyzers and field attributes (searchable/filterable/facetable) to support the queries your application requires.
* Extendability: add custom skills, translation, or additional classification/NER skills to meet specialized requirements.

Links and references

* [Azure Cognitive Search (AI Search) documentation](https://learn.microsoft.com/azure/search/)
* [Azure Blob Storage documentation](https://learn.microsoft.com/azure/storage/blobs/)
* [Azure Cognitive Services documentation](https://learn.microsoft.com/azure/cognitive-services/)
* [Azure OpenAI documentation](https://learn.microsoft.com/azure/cognitive-services/openai/)

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-102-microsoft-certified-azure-ai-engineer-associate/module/668a922e-e573-4bcc-8a97-443ae22d225f/lesson/323fab83-1be5-468e-9d2c-9685d6ebbc9e)
